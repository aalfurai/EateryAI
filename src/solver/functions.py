import pandas as pd
import numpy as np
import math
import copy

from schemas import User, Restaurant, Meal

def score_and_rank_meals(user: User, results: list, k=50, lambda_div=0.3) -> pd.DataFrame:
    # NOTE: Need a fallback if no meals found
    if not results:
        print("ERROR: NO MEALS TO SCORE")
        return pd.DataFrame()  # return empty DataFrame if no meals
    df_candidate_meals = pd.DataFrame(results)
    constraints = user.constraints
    weights = user.weights

    # ------ ORIGINAL SCORING ------
    df_candidate_meals['price_excess'] = (
        (df_candidate_meals['total_price'] - constraints.price)
        .clip(lower=0)
        / constraints.price
    )
    
    
    df_candidate_meals['cal_excess'] = (
        (df_candidate_meals['total_cal'] - constraints.calories)
        .clip(lower=0)
        / constraints.calories
    )
    
    df_candidate_meals['protein_deficit'] = (
        (constraints.protein - df_candidate_meals['total_protein'])
        .clip(lower=0)
        / constraints.protein
    )

    # add penalties for calories in Drink and Add-on categories
    df_candidate_meals['drink_cal_penalty'] = df_candidate_meals['drink_cal'] / constraints.calories
    df_candidate_meals['addon_cal_penalty'] = df_candidate_meals['addon_cal'] / constraints.calories

    # add reward and penalties for other nutrients
    fiber_max = df_candidate_meals['total_fiber'].max()
    fiber_min = df_candidate_meals['total_fiber'].min()
    sugars_max = df_candidate_meals['total_sugars'].max()
    sugars_min = df_candidate_meals['total_sugars'].min()
    sodium_max = df_candidate_meals['total_sodium'].max()
    sodium_min = df_candidate_meals['total_sodium'].min()

    if fiber_max - fiber_min < np.finfo(np.float64).eps:
        df_candidate_meals['fiber_norm'] = 0.5
    else:
        df_candidate_meals['fiber_norm'] = (df_candidate_meals['total_fiber'] - fiber_min) / (fiber_max - fiber_min)

    if sugars_max - sugars_min < np.finfo(np.float64).eps:
        df_candidate_meals['sugars_norm'] = 0.5
    else:
        df_candidate_meals['sugars_norm'] = (df_candidate_meals['total_sugars'] - sugars_min) / (sugars_max - sugars_min)

    if sodium_max - sodium_min < np.finfo(np.float64).eps:
        df_candidate_meals['sodium_norm'] = 0.5
    else:
        df_candidate_meals['sodium_norm'] = (df_candidate_meals['total_sodium'] - sodium_min) / (sodium_max - sodium_min)

    # lower score is better
    df_candidate_meals['score'] = (
        weights.protein * df_candidate_meals['protein_deficit'] +
        weights.calories * df_candidate_meals['cal_excess'] +
        weights.price * df_candidate_meals['price_excess'] -
        weights.fiber * df_candidate_meals['fiber_norm'] +
        weights.sugar * df_candidate_meals['sugars_norm'] +
        weights.sodium * df_candidate_meals['sodium_norm'] +
        weights.drink_cal * df_candidate_meals['drink_cal_penalty'] +
        weights.addon_cal * df_candidate_meals['addon_cal_penalty'] -
        weights.protein * df_candidate_meals['golden_ratio']
    )

    df_sorted = df_candidate_meals.sort_values('score')

    # ------ DIVERSITY SCORING ------
    indices = list(df_sorted.index)
    item_sets = {
        idx: set(df_sorted.loc[idx, 'item_ids'])
        for idx in indices
    }
    selected = []
    candidates = indices.copy()

    while len(selected) < k and candidates:
        best_idx = None
        best_score = float('inf')

        for idx in candidates:
            base_score = df_sorted.loc[idx, 'score']

            if not selected:
                similarity_penalty = 0
            else:
                similarity_penalty = max(
                    len(item_sets[idx] & item_sets[s]) /
                    len(item_sets[idx] | item_sets[s]) 
                    for s in selected
                )

            total_score = base_score + lambda_div * similarity_penalty

            if total_score < best_score:
                best_score = total_score
                best_idx = idx

        if best_idx is None:
            break

        selected.append(best_idx)
        candidates.remove(best_idx)

    result = df_sorted.loc[selected]
    # convert ids back to ints to avoid numpy serialization issues
    for col in ['item_ids', 'Entree_ids', 'Side_ids', 'Drink_ids', 'Addon_ids', 'Dessert_ids']:
        result[col] = result[col].apply(lambda x: [int(i) for i in x])

    result['filled_categories'] = result['filled_categories'].apply(list)
    return result.to_dict(orient='records')

def get_entree_combos(seed_id, entree_combos, is_entree):
    if is_entree:
        return entree_combos[entree_combos['entree_ids'].apply(lambda ids: seed_id in ids)]
    return entree_combos

def get_cand_items(seed_id, category, 
                   entree_combos=None, sides=None, drinks=None, desserts=None, addons=None, 
                   is_entree=False):
    
    if category == 'Entree':
        return get_entree_combos(seed_id, entree_combos, is_entree)
    elif category == 'Side':
        return sides
    elif category == 'Drink':
        return drinks
    elif category == "Dessert":
        return desserts
    elif category == "Add-on":
        return addons

def intermediate_prune(user: User, meals, k=100):
    scores = []
    print(f'  pruning {len(meals)} meals')
    constraints = user.constraints
    weights = user.weights
    for meal in meals:
        price_excess = max(0, meal.total_price - constraints.price) / constraints.price
        cal_excess = max(0, meal.total_cal - constraints.calories) / constraints.calories
        protein_deficit = max(0, constraints.protein - meal.total_protein) / constraints.protein

        drink_penalty = meal.drink_cal / constraints.calories
        addon_penalty = meal.addon_cal / constraints.calories

        golden_ratio = (meal.total_protein * 10) / max(meal.total_cal, 1)

        score = (
            weights.price * price_excess +
            weights.calories * cal_excess +
            weights.protein * protein_deficit +
            weights.drink_cal * drink_penalty +
            weights.addon_cal * addon_penalty -
            weights.protein * golden_ratio * 0.5
        )
        
        scores.append(score)
    
    top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i])[:k]
    return [meals[i] for i in top_k_indices], [scores[i] for i in top_k_indices]


def build_meal(user: User, seed_id, required_categories, restaurant: Restaurant, 
               entree_combos=None, sides=None, drinks=None, desserts=None, addons=None,
               build_full=True) -> list[Meal]:
    PRICE_TOL = round(user.constraints.price * 0.15, 2)
    CAL_TOL = math.ceil(user.constraints.calories * 0.10)

    current_meals = []
    if seed_id == None:
        # if no seed item specified, begin with an empty meal
        meal_state = Meal()
        current_meals.append(meal_state)
        is_entree = False
    
    else:
        seed_item = restaurant.get_item(seed_id)
        category = seed_item.get('category')

        is_entree = (category == 'Entree')
        is_drink = (category == 'Drink')
        is_addon = (category == 'Add-on')

        # if the item is an entree, get all entree combos
        if is_entree and build_full:
            candidate_entrees = get_entree_combos(seed_id=seed_id, entree_combos=entree_combos, is_entree=is_entree)
            for _, combo in candidate_entrees.iterrows():
                meal_state = Meal(
                    item_ids = list(combo['entree_ids']),
                    Entree_ids = list(combo['entree_ids']),
                    Side_ids = [],
                    Drink_ids = [],
                    Addon_ids = [],
                    Dessert_ids = [],
                    total_price = combo['price'],
                    total_cal = combo['calories'],
                    total_protein = combo['protein'],
                    total_fiber = combo['dietary_fiber'],
                    total_sugars = combo['sugars'],
                    total_sodium = combo['sodium'],
                    total_cholesterol = combo['cholesterol'],
                    total_carbohydrates = combo['total_carbohydrates'],
                    total_potassium = combo['potassium'],
                    total_fat = combo['total_fat'],
                    filled_categories = {'Entree'},
                    drink_cal = 0,
                    addon_cal = 0
                )
                current_meals.append(meal_state)
        else:
            meal_state = Meal(
                item_ids = [seed_id],
                Entree_ids = [],
                Side_ids = [],
                Drink_ids = [],
                Addon_ids = [],
                Dessert_ids = [],
                total_price = seed_item.get('price'),
                total_cal = seed_item.get('calories'),
                total_protein = seed_item.get('protein'),
                total_fiber = seed_item.get('dietary_fiber'),
                total_sugars = seed_item.get('sugars'),
                total_sodium = seed_item.get('sodium'),
                total_cholesterol = seed_item.get('cholesterol'),
                total_carbohydrates = seed_item.get('total_carbohydrates'),
                total_potassium = seed_item.get('potassium'),
                total_fat = seed_item.get('total_fat'),
                filled_categories = {seed_item.get('meal_category')},
                drink_cal = 0,
                addon_cal = 0
            )
            getattr(meal_state, f"{category}_ids").append(seed_id)

            if is_drink:
                meal_state.drink_cal = seed_item.get('calories')
            elif is_addon:
                meal_state.addon_cal = seed_item.get('calories')

            current_meals.append(meal_state)

    filled = current_meals[0].filled_categories

    ordered_missing = [
        cat for cat in ["Entree", "Side", "Drink", "Add-on", "Dessert"]
        if cat in required_categories and cat not in filled
    ]

    for category in ordered_missing:
        new_meals = []
        
        for meal in current_meals:
            cand_items = get_cand_items(seed_id=seed_id, category=category, 
                                        entree_combos=entree_combos, 
                                        sides=sides, 
                                        drinks=drinks,
                                        desserts=desserts,
                                        addons=addons,
                                        is_entree=is_entree)
            if cand_items is None or cand_items.empty:
                continue
            cand_items = cand_items[
                (meal.total_price + cand_items['price'] <= user.constraints.price + PRICE_TOL) &
                (meal.total_cal + cand_items['calories'] <= user.constraints.calories + CAL_TOL)
            ]

            for _, item in cand_items.iterrows():
                new_meal: Meal = copy.deepcopy(meal)
                
                if category == 'Entree':
                    new_meal.item_ids.extend(list(item['entree_ids']))
                    new_meal.Entree_ids.extend(list(item['entree_ids']))
                else:
                    new_meal.item_ids.append(item['index'])
                    getattr(new_meal, f"{category}_ids").append(item['index'])

                if category == 'Drink':
                    new_meal.drink_cal += item['calories']
                elif category == 'Add-on':
                    new_meal.addon_cal += item['calories']
                
                new_meal.total_price += item['price']
                new_meal.total_cal += item['calories']
                new_meal.total_protein += item['protein']
                new_meal.total_fiber += item['dietary_fiber']
                new_meal.total_sugars += item['sugars']
                new_meal.total_sodium += item['sodium']
                new_meal.total_cholesterol += item['cholesterol']
                new_meal.total_carbohydrates += item['total_carbohydrates']
                new_meal.total_potassium += item['potassium']
                new_meal.total_fat += item['total_fat']
                new_meal.filled_categories.add(category)

                new_meal.total_price = round(new_meal.total_price, 2)
                new_meal.golden_ratio = (new_meal.total_protein * 10) / max(new_meal.total_cal, 1)
                new_meals.append(new_meal)

        top_k_meals, meal_scores = intermediate_prune(user, new_meals, k=200)
        sim_matrix = precompute_similarity(top_k_meals)
        current_meals = diversity_prune(top_k_meals, meal_scores, sim_matrix)

    return current_meals


def precompute_similarity(meals):
    n = len(meals)
    # store in a matrix for lookup later
    sim_matrix = np.zeros((n,n))

    # convert to sets
    item_sets = [set(m.item_ids) for m in meals]
    sizes = [len(s) for s in item_sets]

    # calculate Jaccard index and store
    for i in range(n):
        for j in range(i + 1, n):
            inter = len(item_sets[i] & item_sets[j])
            union = sizes[i] + sizes[j] - inter
            
            sim_matrix[i, j] = inter / union if union > 0 else 0
            sim_matrix[j, i] = sim_matrix[i, j]
    
    return sim_matrix


def diversity_prune(meals, scores, sim_matrix, k=100, lambda_div=0.3):
    selected = []
    candidates = list(range(len(meals)))
    
    for _ in range(k):
        best = None
        best_score = float('inf')
        
        for i in candidates:
            base_score = scores[i]
            
            if not selected:
                similarity_penalty = 0
            else:
                sims = [sim_matrix[i][j] for j in selected]
                
                # fallback for no diversity
                if max(sims) - min(sims) < np.finfo(np.float64).eps:
                    similarity_penalty = 0   # ignore diversity
                else:
                    similarity_penalty = max(sims)
            
            total = base_score + lambda_div * similarity_penalty
            
            if total < best_score:
                best = i
                best_score = total
        
        if best is None:
            break

        selected.append(best)
        candidates.remove(best)
    
    return [meals[i] for i in selected]