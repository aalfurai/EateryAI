import itertools
import pandas as pd
from fastapi import HTTPException
from backend import queries
from schemas.user import User
from schemas.restaurant import Restaurant
from schemas.meal import Meal
from collections import defaultdict


class DataService:
    def __init__(self):
        self._restaurant_cache = {}
        self._users: dict[str, User] = {}  # In-memory user store for demo purposes; replace with DB in production
        self._saved_meals: dict[str, list] = {}  # In-memory store for saved meals

    # ─────────────────────────────────────────────
    # User
    # ─────────────────────────────────────────────

    def load_user(self, user_id: str) -> User:
        user = self._users.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
        return user
    
    def check_user_exists(self, user_id: str) -> bool:
        return user_id in self._users
    
    def add_user(self, user: User):
        self._users[user.user_id] = user

    def update_user_constraints(self, user_id: str, **kwargs) -> User:
        # TODO: replace with DB update query and loop logic
        user = self.load_user(user_id)
        user.update_constraints(**kwargs)
        self._save_user(user)
        return user

    def update_user_weights(self, user_id: str, **kwargs) -> User:
        # TODO: replace with DB update query and loop logic
        user = self.load_user(user_id)
        user.update_weights(**kwargs)
        self._save_user(user)
        return user

    def _save_user(self, user: User):
        # TODO: DB WRITE
        # db.execute(
        #     "UPDATE users SET constraints = %s, weights = %s WHERE user_id = %s",
        #     (json.dumps(user.constraints.to_dict()), 
        #      json.dumps(user.weights.to_dict()),
        #      user.user_id)
        # )
        pass

    # ─────────────────────────────────────────────
    # Saved Meals
    # ─────────────────────────────────────────────

    def get_saved_meals(self, user_id: str) -> list:
        return self._saved_meals.get(user_id, [])

    def save_meal(self, user_id: str, meal: Meal) -> int:
        self._saved_meals.setdefault(user_id, []).append(meal)
        return len(self._saved_meals[user_id])

    def delete_saved_meal(self, user_id: str, meal_index: int) -> dict:
        meals = self._saved_meals.get(user_id, [])
        if 0 <= meal_index < len(meals):
            return meals.pop(meal_index)
        raise HTTPException(status_code=404, detail="Saved meal not found")
    
    # ─────────────────────────────────────────────
    # Restaurant
    # ─────────────────────────────────────────────

    def load_restaurant(self, conn, restaurant_name: str) -> Restaurant:
        key = restaurant_name.lower()
        if key in self._restaurant_cache:
            return self._restaurant_cache[key]

        # load from db
        rows = queries.find_restaurant_by_name(conn, restaurant_name)
        if not rows:
            raise ValueError(f"Restaurant '{restaurant_name}' not found")
        
        # Update restaurant name to match DB
        restaurant_id, restaurant_name = self._resolve_restaurant_id(conn, restaurant_name)
        restaurant = self._build_solver_restaurant(conn, restaurant_id, restaurant_name)
        self._restaurant_cache[key] = restaurant
        return restaurant
    
    def _resolve_restaurant_id(self, conn, restaurant_name: str) -> str:
        """Look up restaurant_id by name or raise 404."""
        rows = queries.find_restaurant_by_name(conn, restaurant_name)
        if not rows:
            raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_name}' not found")
        return rows[0]["restaurant_id"], rows[0]["restaurant_name"]

    def _build_solver_restaurant(self, conn, restaurant_id: str, restaurant_name: str) -> Restaurant:
        """
        Load items from DB and assemble a Restaurant object with category lists
        and entree combos — everything the solver needs, with no DataService.
        """
        rows = queries.get_menu_items_for_solver(conn, restaurant_id)

        menu = defaultdict(list)
        entrees, sides, drinks, desserts, addons = [], [], [], [], []
        for idx, row in enumerate(rows):
            item = {
                "index":          idx,
                "item_id":        row["item_id"],
                "menu_item_name": row["menu_item_name"],
                "category":       row["category"],
                "price":          float(row["price"]),
                "calories":       int(row["calories"]),
                "protein":        int(row["protein"]),
                "dietary_fiber":  int(row["dietary_fiber"]),
                "sugars":         int(row["sugars"]),
                "sodium":         int(row["sodium"]),
                "cholesterol":    int(row["cholesterol"]),
                "total_carbohydrates": int(row["total_carbohydrates"]),
                "potassium":      int(row["potassium"]),
                "total_fat":      int(row["total_fat"]),
                "serving_size":   row["serving_size"],
            }
            menu[row["item_id"]].append(item)
            match item["category"]:
                case "Entree":  entrees.append(item)
                case "Side":    sides.append(item)
                case "Drink":   drinks.append(item)
                case "Dessert": desserts.append(item)
                case "Add-On":  addons.append(item)

        entree_combos = DataService._calculate_entree_combos(entrees)
        entrees = pd.DataFrame(entrees)
        sides = pd.DataFrame(sides)
        drinks = pd.DataFrame(drinks)
        desserts = pd.DataFrame(desserts)
        addons = pd.DataFrame(addons)

        return Restaurant(
            name=restaurant_name,
            menu=menu,
            entrees=entrees,
            sides=sides,
            drinks=drinks,
            desserts=desserts,
            addons=addons,
            entree_combos=entree_combos,
        )

    # def load_item(self, restaurant: Restaurant, item_id: str) -> dict:
    #     item = restaurant.get_item(item_id)
    #     if item is None:
    #         raise KeyError(f"Item {item_id} not found in {restaurant.name}")
    #     return item

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────

    # @staticmethod
    # def _build_category_lists(menu: dict) -> tuple:
    #     """Split menu into category-specific lists in a single pass."""
    #     entrees, sides, drinks, desserts, addons = [], [], [], [], []
    #     for item in menu.values():
    #         match item['category']:
    #             case 'Entree':
    #                 entrees.append(item)
    #             case 'Side':
    #                 sides.append(item)
    #             case 'Drink':
    #                 drinks.append(item)
    #             case 'Dessert':
    #                 desserts.append(item)
    #             case 'Add-On':
    #                 addons.append(item)
    #     return (
    #         pd.DataFrame(entrees),
    #         pd.DataFrame(sides),
    #         pd.DataFrame(drinks),
    #         pd.DataFrame(desserts),
    #         pd.DataFrame(addons)
    #     )

    @staticmethod
    def _calculate_entree_combos(entrees: list, max_count=2) -> pd.DataFrame:
        """Calculate all valid entree combinations up to max_count items."""
        MAX_PRICE    = 100.0
        MAX_CALORIES = 3000

        entrees_df = pd.DataFrame(entrees)

        prices      = entrees_df['price'].to_numpy()
        calories    = entrees_df['calories'].to_numpy()
        proteins    = entrees_df['protein'].to_numpy()
        fibers      = entrees_df['dietary_fiber'].to_numpy()
        sugars      = entrees_df['sugars'].to_numpy()
        sodiums     = entrees_df['sodium'].to_numpy()
        cholesterol = entrees_df['cholesterol'].to_numpy()
        carbs       = entrees_df['total_carbohydrates'].to_numpy()
        potassium   = entrees_df['potassium'].to_numpy()
        fats        = entrees_df['total_fat'].to_numpy()
        indices     = entrees_df['index'].to_numpy()
        names       = entrees_df['menu_item_name'].to_numpy()
        sizes       = entrees_df['serving_size'].to_numpy()

        entree_combos = []
        combo_id = 1

        for k in range(1, max_count+1):
            for combo_idx in itertools.combinations_with_replacement(range(len(entrees)), k):
                total_price    = prices[list(combo_idx)].sum()
                total_calories = calories[list(combo_idx)].sum()
                if total_price > MAX_PRICE or total_calories > MAX_CALORIES:
                    continue

                i = list(combo_idx)
                entree_combos.append({
                    "combo_id":             combo_id,
                    "entree_ids":           tuple(indices[i]),
                    "entree_names":         tuple(names[i]),
                    "n_entrees":            k,
                    "price":                round(total_price, 2),
                    "calories":             total_calories,
                    "protein":              proteins[i].sum(),
                    "dietary_fiber":        fibers[i].sum(),
                    "sugars":               sugars[i].sum(),
                    "sodium":               sodiums[i].sum(),
                    "cholesterol":          cholesterol[i].sum(),
                    "total_carbohydrates":  carbs[i].sum(),
                    "potassium":            potassium[i].sum(),
                    "total_fat":            fats[i].sum(),
                    "serving_size_per_item":tuple(sizes[i]),
                })
                combo_id += 1
        
        return pd.DataFrame(entree_combos)

    # def _serialize_meals(meals: list) -> list:
    #     """Make meal dicts JSON-safe (sets -> lists)."""
    #     result = []
    #     for meal in meals:
    #         m = dict(meal)
    #         if isinstance(m.get("filled_categories"), set):
    #             m["filled_categories"] = list(m["filled_categories"])
    #         result.append(m)
    #     return result
