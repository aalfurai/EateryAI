import json
import itertools
from pathlib import Path
import httpx
from schemas.user import User
from schemas.restaurant import Restaurant


PATH = "../restaurants_data_manual_recat.json"

class DataService:
    def __init__(self, base_url: str | None = None, data_path: str = PATH):
        self.base_url = base_url
        self.data_path = data_path # NOTE: used in place of db access for now
        self._menu_cache = {}
        self._restaurant_cache = {}

    def load_user(self, user_id: str) -> User:
        r = httpx.get(f"{self.base_url}/users/{user_id}")
        r.raise_for_status()
        return User.from_dict(r.json())

    def load_restaurant(self, restaurant_name: str) -> Restaurant:
        try:
            r = httpx.get(f"{self.base_url}/menu/{restaurant_name}")
            r.raise_for_status()
            data = r.json()
            return Restaurant.from_dict(data)
        except:
            pass

        # if api call fails, fallback on local json
        key = restaurant_name.lower()
        if key in self._restaurant_cache:
            return self._restaurant_cache[key]

        menu = self._load_menu(restaurant_name)
        entrees, sides, drinks, desserts, addons = self._build_category_lists(menu)

        print(f"  Computing entree combos...", end="", flush=True)
        entree_combos = self._calculate_entree_combos(entrees)
        print(f" {len(entree_combos)} combos")

        restaurant = Restaurant(
            name          = restaurant_name,
            menu          = menu,
            entrees       = entrees,
            sides         = sides,
            drinks        = drinks,
            desserts      = desserts,
            addons        = addons,
            entree_combos = entree_combos,
        )
        self._restaurant_cache[key] = restaurant
        return restaurant

    def load_item(self, restaurant: Restaurant, item_id: str) -> dict:
        item = restaurant.get_item(item_id)
        if item is None:
            raise KeyError(f"Item {item_id} not found in {restaurant.name}")
        return item

    # menu loading and caching
    def _load_menu(self, restaurant_name: str) -> dict:
        """Load and cache the raw menu for a restaurant."""
        if not self._menu_cache:
            raw = self._read_json()
            self._menu_cache = raw

        print(f"\n  Loading {restaurant_name} data...", end="", flush=True)
        menu = self._parse_menu(self._menu_cache, restaurant_name)
        print(f" {len(menu)} items loaded")
        return menu

    def _read_json(self) -> list:
        path = Path(self.data_path)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    
    # data loading
    @staticmethod
    def _parse_menu(data: list, restaurant_name: str) -> dict:
        """Returns a dict of restaurant items"""
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

    @staticmethod
    def _build_category_lists(menu: dict) -> tuple:
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
    @staticmethod
    def _calculate_entree_combos(entrees: list, max_count=2) -> list:
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