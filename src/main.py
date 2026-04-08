from fastapi import FastAPI
from contextlib import asynccontextmanager
import json
from solver.data import enter_restaurant


app = FastAPI()
restaurant_cache = {}

def get_restaurant_data(restaurant_name: str):
    if restaurant_name not in restaurant_cache:
        restaurant_cache[restaurant_name] = enter_restaurant(restaurant_name)
    return restaurant_cache[restaurant_name]

@app.get("/")
async def root():
    return {"message": "Welcome to Eatery"}

@app.get("/menu")
def menu():
    with open("../restaurants_data_manual_recat.json") as file:
        menu_data = json.load(file)
    return menu_data

@app.get("/menu/{restaurant}/{item_id}")
def menu(restaurant: str, item_id: int):
    restaurant_data = get_restaurant_data(restaurant)
    if restaurant_data is None:
        return {"error": f"Restaurant '{restaurant}' not found"}
    item = restaurant_data.get_item(item_id)
    if item is None:
        return {"error": f"Item ID '{item_id}' not found in restaurant '{restaurant}'"}
    return item

@app.get("/menu/{restaurant}")
def menu(restaurant: str):
    restaurant_data = get_restaurant_data(restaurant)
    if restaurant_data is None:
        return {"error": f"Restaurant '{restaurant}' not found"}
    return restaurant_data.to_json()