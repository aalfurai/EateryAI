from fastapi import HTTPException
from schemas.restaurant import Restaurant
import json

restaurant_cache = {}
PATH = "../restaurants_data_manual_recat.json"

def enter_restaurant(self, restaurant_name: str):
    """Load restaurant data and build category lists."""
    print(f'\n  Loading {restaurant_name.lower()} data...', end='', flush=True)
    menu = self.load_restaurant_data(PATH, restaurant_name)
    if not menu:
        raise ValueError(f"No data found for restaurant: {restaurant_name}")
    entrees, sides, drinks, desserts, addons = self.build_category_lists(menu)
    print(f' {len(menu)} items loaded')
    print(f'  Computing entree combos...', end='', flush=True)
    entree_combos = self.calculate_entree_combos(entrees)
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

def get_restaurant_data(restaurant_name: str):
    if restaurant_name not in restaurant_cache:
        try:
            restaurant_cache[restaurant_name] = enter_restaurant(restaurant_name)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_name}' not found") from e
    return restaurant_cache[restaurant_name]

def get_all_menus():
    if "all_menus" not in restaurant_cache:
        with open("../restaurants_data_manual_recat.json", encoding="utf-8") as file:
            restaurant_cache["all_menus"] = json.load(file)
    return restaurant_cache["all_menus"]