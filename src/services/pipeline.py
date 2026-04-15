from schemas.meal import Meal
from schemas.restaurant import Restaurant
from schemas.user import User
import solver.functions as solver
from services.data import DataService

class PipelineService:

    def __init__(self, data_service: DataService):
        self.data = data_service

    def recommend_from_seed(
        self, user_id: str, restaurant_name: str, seed_id: str = None
    ) -> list[Meal]:
        """User pre-selected an item; build the best combo around it."""
        user       = self.data.load_user(user_id)
        restaurant = self.data.load_restaurant(restaurant_name)
        anchor     = self.data.load_item(restaurant_name, seed_id)
        return self._build_top_combos(user, restaurant, anchor_item=anchor)

    def _build_top_combos(self, user: User, restaurant: Restaurant, anchor_item: dict | None) -> list[Meal]:

        meals = solver.build_meal(
            user=user,
            seed_id=anchor_item['index'] if anchor_item else None,
            required_categories={'Entree', 'Side', 'Drink'},
            restaurant=restaurant.menu,
            entree_combos=restaurant.entree_combos,
            sides=restaurant.sides,
            drinks=restaurant.drinks,
            desserts=restaurant.desserts,
            addons=restaurant.addons,
            build_full=bool(anchor_item))

        ranked = solver.score_and_rank_meals(user, meals)
        return ranked[:3]