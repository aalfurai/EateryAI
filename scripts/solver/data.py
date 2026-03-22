import json
import itertools
from schemas.restaurant import Restaurant

# MAIN FILE IN PLACE OF DB ACCESS
PATH = "../restaurants_data_manual_recat.json"

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
    # NOTE: replace for db query
    for item in data:
        if item.get('restaurant_name', '').lower() != restaurant_name.lower():
            continue
        nutrition = item.get('nutrition_info', {})
        items[idx] = {
            'index':          idx,
            'item_id':        item.get('item_id'),
            'menu_item_name': item.get('menu_item_name', ''),
            'price':          float(item.get('price', 0.0)),
            'calories':       int(nutrition.get('calories', 0)),
            'protein':        int(nutrition.get('protein', 0)),
            'serving_size':   nutrition.get('serving_size', ''),
            'category':       item.get('category')
        }
        idx += 1
    return items

def build_category_lists(menu: dict) -> tuple:
    """Split menu into category-specific lists in a single pass."""
    entrees, sides, drinks, desserts, addons = [], [], [], [], []
    for item in menu.values():
        match item['category']:
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

def enter_restaurant(restaurant_name: str):
    """Load restaurant data and build category lists."""
    print(f'\n  Loading {restaurant_name.lower()} data...', end='', flush=True)
    menu = load_restaurant_data(PATH, restaurant_name)
    entrees, sides, drinks, desserts, addons = build_category_lists(menu)
    print(f' {len(menu)} items loaded')
    print(f'  Computing entree combos...', end='', flush=True)
    entree_combos = calculate_entree_combos(entrees)
    print(f' {len(entree_combos)} combos\n')
    
    return Restaurant(
        name=restaurant_name,
        menu=menu,
        entrees=entrees,
        sides=sides,
        drinks=drinks,
        desserts=desserts,
        addons=addons,
        entree_combos=entree_combos
    )
