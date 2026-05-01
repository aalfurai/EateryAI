from fastapi import HTTPException

from schemas.meal import Meal
from schemas.restaurant import Restaurant
from schemas.user import User
import solver.functions as solver
from services.data import DataService
import pandas as pd

class PipelineService:

    def __init__(self, data_service: DataService):
        self.data = data_service

    def recommend(self, conn, user: User, restaurant_name: str, seed_id: str = None, required_categories: set[str] = None) -> list[Meal]:
        restaurant = self.data.load_restaurant(conn, restaurant_name)
        seed       = restaurant.get_item(int(seed_id)) if seed_id else None
        return self._build_top_combos(user, restaurant, seed_item=seed, required_categories=required_categories)

    def _build_top_combos(self, user: User, restaurant: Restaurant, seed_item: dict | None, required_categories: set[str]) -> pd.DataFrame:
        try:
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")
        
    # def recommend_for_you(self, conn, user: User) -> list[Meal]:
    #     restaurants = queries.get_all_restaurants(conn)


        