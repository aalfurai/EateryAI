import httpx
from schemas.user import User
from schemas.restaurant import Restaurant

class DataService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def load_user(self, user_id: str) -> User:
        r = httpx.get(f"{self.base_url}/users/{user_id}")
        r.raise_for_status()
        return User.from_dict(r.json())

    def load_restaurant(self, restaurant_name: str) -> Restaurant:
        r = httpx.get(f"{self.base_url}/menu/{restaurant_name}")
        r.raise_for_status()
        return Restaurant.from_dict(r.json())

    def load_item(self, restaurant_name: str, item_id: str) -> dict:
        r = httpx.get(f"{self.base_url}/menu/{restaurant_name}/{item_id}")
        r.raise_for_status()
        return r.json()

    # def load_restaurant_by_item(self, item_id: str) -> Restaurant:
    #     """Fetch the restaurant that owns a given item."""
    #     r = httpx.get(f"{self.base_url}/items/{item_id}/restaurant")
    #     r.raise_for_status()
    #     return Restaurant.from_dict(r.json())