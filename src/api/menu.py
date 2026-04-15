from fastapi import APIRouter, HTTPException
from solver.data import enter_restaurant
from dependencies import get_all_menus


router = APIRouter(prefix="/menu", tags=["menu"])
restaurant_cache = {}

def get_restaurant_data(restaurant_name: str):
    if restaurant_name not in restaurant_cache:
        try:
            restaurant_cache[restaurant_name] = enter_restaurant(restaurant_name)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_name}' not found") from e
    return restaurant_cache[restaurant_name]

@router.get("/")
def menu():
    return get_all_menus()

@router.get("/{restaurant}/{item_id}")
def menu(restaurant: str, item_id: int):
    restaurant_data = get_restaurant_data(restaurant)
    try:
        item = restaurant_data.get_item(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item ID '{item_id}' not found in restaurant '{restaurant}'")
    return item

@router.get("/{restaurant}")
def menu(restaurant: str):
    restaurant_data = get_restaurant_data(restaurant)
    return restaurant_data.to_dict()