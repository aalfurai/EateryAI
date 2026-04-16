import itertools
import copy

from schemas import User, Restaurant

def score_and_rank_meals(user: User, results: list) -> list:
    scored = []
    diverse = set()
    for meal in results:
        # quick fix to diversify results
        # NOTE: find a way to diversify results (if required categories is 1 then this breaks)
        if frozenset((meal['item_ids'][0], meal['item_ids'][1])) in diverse or frozenset((meal['item_ids'][0], meal['item_ids'][2])) in diverse:
            continue
        diverse.add(frozenset((meal['item_ids'][0], meal['item_ids'][1])))
        diverse.add(frozenset((meal['item_ids'][0], meal['item_ids'][2])))

        c = user.constraints
        w = user.weights

        protein_deficit = max(0, c.protein - meal['total_protein']) / c.protein
        cal_excess = max(0, meal['total_cal']   - c.calories)   / c.calories
        price_excess = max(0, meal['total_price'] - c.price) / c.price
        cheap_bonus = max(0, c.price - meal['total_price']) / c.price
        golden_ratio = (meal['total_protein'] * 10) / max(meal['total_cal'], 1)
        score = (
            w.protein * protein_deficit +
            w.calories * cal_excess +
            w.protein * price_excess -
            w.protein * cheap_bonus -
            w.protein * golden_ratio
        )
        scored.append({**meal, 'score': score, 'golden_ratio': golden_ratio})
    return sorted(scored, key=lambda m: m['score'])

def get_entree_combos(seed_id, entree_combos, is_entree):
    if is_entree:
        return [combo for combo in entree_combos if seed_id in combo['entree_ids']]
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

def intermediate_prune(user: User, meals, k=50):
    scores = []
    print(f'  pruning {len(meals)} meals')
    c = user.constraints
    w = user.weights
    for meal in meals:
        # cheaper is always better
        price_efficiency = meal['total_price'] / c.price
        # calories should always be close to the user's target
        cal_dev = abs(meal['total_cal'] - c.calories) / c.calories
        # protein should always meet or exceed the user's target
        protein_score = 1 / (meal['total_protein'] / c.protein)
        golden_ratio = (meal['total_protein'] * 10) / max(meal['total_cal'], 1)

        # lower score is better
        score = w.price * price_efficiency + w.calories * cal_dev + w.protein * (protein_score - golden_ratio)
        scores.append(score)
    
    top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i])[:k]
    return [meals[i] for i in top_k_indices]
    
# NOTE: this function should be broken down more
def build_meal(user: User, seed_id, required_categories, restaurant: Restaurant, 
               entree_combos=None, sides=None, drinks=None, desserts=None, addons=None,
               build_full=True):
    c = user.constraints

    seed_item = restaurant.get_item(int(seed_id))

    current_meals = []

    is_entree = (seed_item.get('meal_category') == 'Entree')

     # if the item is an entree, get all entree combos
    if is_entree and build_full:
        candidate_entrees = get_entree_combos(seed_id=seed_id, entree_combos=entree_combos, is_entree=is_entree)
        for combo in candidate_entrees:
            meal_state = {
                'item_ids': list(combo['entree_ids']),
                'total_price': combo['price'],
                'total_cal': combo['calories'],
                'total_protein': combo['protein'],
                'filled_categories': {'Entree'}
            }
            current_meals.append(meal_state)
    else:
        meal_state = {
            'item_ids': [seed_id],
            'total_price': seed_item.get('price'),
            'total_cal': seed_item.get('calories'),
            'total_protein': seed_item.get('protein'),
            'filled_categories': {seed_item.get('meal_category')}
        }
        current_meals.append(meal_state)

    missing_categories = required_categories - current_meals[0].get('filled_categories')

    for category in missing_categories:
        new_meals = []
        
        for meal in current_meals:
            cand_items = get_cand_items(seed_id=seed_id, category=category, 
                                        entree_combos=entree_combos, 
                                        sides=sides, 
                                        drinks=drinks,
                                        desserts=desserts,
                                        addons=addons,
                                        is_entree=is_entree)

            cand_items = [
                item for item in cand_items
                if meal['total_price'] + item['price'] <= c.price + c.get_price
                and meal['total_cal']  + item['calories'] <= c.calories + c.get_calories
            ]

            for item in cand_items:
                new_meal = copy.deepcopy(meal)
                
                if category == 'Entree':
                    new_meal['item_ids'].extend(item['entree_ids'])
                else:
                    new_meal['item_ids'].append(item['index'])
                
                new_meal['total_price'] += item['price']
                new_meal['total_cal'] += item['calories']
                new_meal['total_protein'] += item['protein']
                new_meal['filled_categories'].add(category)

                new_meal['total_price'] = round(new_meal['total_price'], 2)
                new_meals.append(new_meal)

        current_meals = intermediate_prune(user, new_meals)
    
    return current_meals

# some functions for visualization
def get_item_name(restaurant, id):
    return restaurant[id]['menu_item_name']

def get_item_price(restaurant, id):
    return restaurant[id]['price']

def get_item_calories(restaurant, id):
    return restaurant[id]['calories']

def get_item_protein(restaurant, id):
    return restaurant[id]['protein']

def display_meal(restaurant, meal):
    print(f"Items in this meal:")
    for id in meal['item_ids']:
        print(f"\t{get_item_name(restaurant, id)}, ${get_item_price(restaurant, id):.2f}, {get_item_calories(restaurant, id)}, {get_item_protein(restaurant, id)}")
    print(f"Total price: ${meal['total_price']}")
    print(f"Total calories: {meal['total_cal']}")
    print(f"Total_protein: {meal['total_protein']}")
    print(f"Golden ratio: {meal['total_protein'] * 10 / meal['total_cal']:.2f}%\n")


# functions from demo
def select_categories() -> set:

    # NOTE: should add option to request multiple categories
    options = [
        ('Entree',  True),
        ('Side',    True),
        ('Drink',   True),
        ('Dessert', False),
        ('Add-on',  False),
    ]

    categories = [] # list of selected categories

    print(f'\n  Selected: {", ".join(sorted(categories))}\n')
    return categories