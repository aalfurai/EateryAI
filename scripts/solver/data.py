import json
import math
import itertools

# MAIN FILE IN PLACE OF DB ACCESS
PATH = "EateryAI/restaurants_data_manual_recat.json"

# category constants

ENTREE_CATEGORIES = {'Classic Chicken', 'Breakfast', 'Cool Wraps', 'Salads'}
ADDON_CATEGORIES  = {'Salad Dressings', 'Sauces'}
KIDS_MEAL         = "Kid's Meal"
HASH_BROWN_IDX    = 90  # manually assigned Side

# category mapping 

def map_category(raw: str, name: str, idx: int) -> str:
    """Manually map raw JSON categories to meal categories."""
    if raw in ENTREE_CATEGORIES:
        return 'Entree'
    if raw == 'Sides':
        return 'Side'
    if raw == 'Beverages':
        return 'Drink'
    if raw == 'Desserts':
        return 'Dessert'
    if raw in ADDON_CATEGORIES:
        return 'Add-on'
    if raw == KIDS_MEAL:
        name_lower = name.lower()
        if 'meal' in name_lower:
            return 'Entree'
        if 'milk' in name_lower:
            return 'Drink'
        return 'Side'
    if idx == HASH_BROWN_IDX:
        return 'Side'
    return 'Other'

# data loading

def load_restaurant_data(path: str, restaurant_name: str) -> dict:
    """Returns a dict of CFA items"""
    try:
        with open(path) as f:
                data = json.load(f)
    except FileNotFoundError:
        print(f'\n  x  File not found: {path}')
        return {}

    items = {}
    idx = 0
    for item in data:
        if item.get('restaurant_name', '').lower() != 'chick-fil-a':
            continue
        nutrition = item.get('nutrition_info', {})
        name = item.get('menu_item_name', '')
        raw_category = item.get('category', '')
        items[idx] = {
            'index':          idx,
            'item_id':        item.get('item_id'),
            'menu_item_name': name,
            'price':          float(item.get('price', 0.0)),
            'calories':       int(nutrition.get('calories', 0)),
            'protein':        int(nutrition.get('protein', 0)),
            'serving_size':   nutrition.get('serving_size', ''),
            'meal_category':  map_category(raw_category, name, idx),
            'category':       raw_category,
        }
        idx += 1
    return items

def build_category_lists(menu: dict) -> tuple:
    """Split menu into category-specific lists in a single pass."""
    entrees, sides, drinks, desserts, addons = [], [], [], [], []
    for item in menu.values():
        match item['meal_category']:
            case 'Entree':
                entrees.append(item)
            case 'Side':
                sides.append(item)
            case 'Drink':
                drinks.append(item)
            case 'Dessert':
                desserts.append(item)
            case 'Add-On':
                addons.append(item)
    return entrees, sides, drinks, desserts, addons

# entree combos

def calculate_entree_combos(entrees: list, max_count=2) -> list:
    """Calculate all valid entree combinations up to max_count items."""
    MAX_PRICE    = 100.0
    MAX_CALORIES = 3000
    MAX_PROTEIN = 500

    combos   = []
    combo_id = 1
    for k in range(1, max_count + 1):
        for combo in itertools.combinations_with_replacement(entrees, k):
            total_price    = sum(i['price']    for i in combo)
            total_calories = sum(i['calories'] for i in combo)
            total_protein  = sum(i['protein']  for i in combo)
            if total_price > MAX_PRICE or total_calories > MAX_CALORIES:
                continue
            combos.append({
                'combo_id':          combo_id,
                'entree_ids':        tuple(i['index'] for i in combo),
                'entree_names':      tuple(i['menu_item_name'] for i in combo),
                'n_entrees':         k,
                'price':             round(total_price, 2),
                'calories':          total_calories,
                'protein':           total_protein,
            })
            combo_id += 1
    return combos

def enter_restaurant(restaurant_name: str) -> dict:
    """Load restaurant data and build category lists."""
    print(f'\n  Loading {restaurant_name.lower()} data...', end='', flush=True)
    menu = load_restaurant_data(PATH, restaurant_name)
    entrees, sides, drinks, desserts, addons = build_category_lists(menu)
    print(f' {len(menu)} items loaded')
    print(f'  Computing entree combos...', end='', flush=True)
    entree_combos = calculate_entree_combos(entrees)
    print(f' {len(entree_combos)} combos\n')
    return menu, entrees, entree_combos, sides, drinks, desserts, addons
