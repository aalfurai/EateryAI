from solver.data import enter_restaurant
import json

restaurant_cache = {}

def get_restaurant_data(restaurant_name: str):
    name = restaurant_name.replace("-", " ")
    if name not in restaurant_cache:
        restaurant_cache[name] = enter_restaurant(name)
    return restaurant_cache[name]

def get_all_menus():
    if "all_menus" not in restaurant_cache:
        with open("../restaurants_data_manual_recat.json") as file:
            restaurant_cache["all_menus"] = json.load(file)
    return restaurant_cache["all_menus"]