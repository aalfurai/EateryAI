from schemas.meal import Meal
from schemas.restaurant import Restaurant
from schemas.user import User
import solver.functions as solver
from services.data import DataService
from services.session import SessionService
import pandas as pd

class PipelineService:

    def __init__(self, data_service: DataService):
        self.data = data_service
        self.session = SessionService(data_service)

    def start_session(self, user_id: str) -> User:
        return self.session.load_user(user_id)

    def recommend_from_seed(self, restaurant_name: str, seed_id: str = None, required_categories: set[str] = None) -> list[Meal]:
        restaurant = self.data.load_restaurant(restaurant_name)
        seed       = restaurant.get_item(int(seed_id)) if seed_id else None
        meals = self._build_top_combos(self.session.user, restaurant, seed_item=seed, required_categories=required_categories)
        return meals

    def _build_top_combos(self, user: User, restaurant: Restaurant, seed_item: dict | None, required_categories: set[str]) -> pd.DataFrame:

        meals = solver.build_meal(
            user=user,
            seed_id=seed_item['index'] if seed_item else None,
            required_categories=required_categories,
            restaurant=restaurant,
            entree_combos=restaurant.entree_combos,
            sides=restaurant.sides,
            drinks=restaurant.drinks,
            desserts=restaurant.desserts,
            addons=restaurant.addons,
            build_full=bool(seed_item))
        
        ranked = solver.score_and_rank_meals(user, meals)
        return ranked[:3]