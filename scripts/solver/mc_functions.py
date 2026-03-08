def get_entree_combos(seed_id, df_entree_combos, is_entree):
    if is_entree:
        mask = df_entree_combos['entree_ids'].apply(lambda ids: seed_id in ids)
        return df_entree_combos[mask]
    else:
        return df_entree_combos

def get_cand_items(seed_id, category, 
                   df_entree_combos=None, df_sides=None, df_drinks=None, df_desserts=None, df_addons=None, 
                   is_entree=False):
    
    if category == 'Entree':
        return get_entree_combos(seed_id, df_entree_combos, is_entree)
    elif category == 'Side':
        return df_sides
    elif category == 'Drink':
        return df_drinks
    elif category == "Dessert":
        return df_desserts
    elif category == "Add-on":
        return df_addons

def intermediate_prune(meals, k=50):
    scores = []
    print(len(meals))
    for meal in meals:
        # cheaper is always better
        price_efficiency = meal['total_price'] / USER_PRICE
        # calories should always be close to the user's target
        cal_dev = abs(meal['total_cal'] - USER_CAL) / USER_CAL
        # protein should always meet or exceed the user's target
        protein_score = 1 / (meal['total_protein'] / USER_PROTEIN)
        golden_ratio = (meal['total_protein'] * 10) / max(meal['total_cal'], 1)

        # lower score is better
        score = W_PRICE * price_efficiency + W_CAL * cal_dev + W_PROTEIN * (protein_score - golden_ratio)
        scores.append(score)
    
    scores = np.array(scores)
    sorted_indices = scores.argsort()
    top_k_indices = sorted_indices[:k]
    return [meals[i] for i in top_k_indices]
    
def build_meal(seed_id, required_categories, df_restaurant, 
               df_entree_combos=None, df_sides=None, df_drinks=None, df_desserts=None, df_addons=None,
               build_full=True):
    
    seed_item = df_restaurant.loc[seed_id].to_dict()

    current_meals = []

    is_entree = (seed_item.get('meal_category') == 'Entree')

     # if the item is an entree, get all entree combos
    if is_entree and build_full:
        candidate_entrees = get_entree_combos(seed_id=seed_id, df_entree_combos=df_entree_combos, is_entree=is_entree)
        for _, combo in candidate_entrees.iterrows():
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
                                        df_entree_combos=df_entree_combos, 
                                        df_sides=df_sides, 
                                        df_drinks=df_drinks,
                                        df_desserts=df_desserts,
                                        df_addons=df_addons,
                                        is_entree=is_entree)

            cand_items = cand_items[
                (meal['total_price'] + cand_items['price'] <= USER_PRICE + PRICE_TOL) &
                (meal['total_cal'] + cand_items['calories'] <= USER_CAL + CAL_TOL)
            ]

            for _, item in cand_items.iterrows():
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

        current_meals = intermediate_prune(new_meals)
    
    return current_meals