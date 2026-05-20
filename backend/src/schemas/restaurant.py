from dataclasses import dataclass, field

@dataclass
class SQLData:
    item_id:        str
    menu_item_id:   str
    restaurant_id:  int
    menu_item_name: str
    category:       str
    price:          float
    golden_ratio:   float
    ai_description: str

@dataclass
class Restaurant:
    name:          str
    menu:          dict  = field(default_factory=dict)
    entrees:       list  = field(default_factory=list)
    sides:         list  = field(default_factory=list)
    drinks:        list  = field(default_factory=list)
    desserts:      list  = field(default_factory=list)
    addons:        list  = field(default_factory=list)
    entree_combos: list  = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            raise ValueError("Restaurant name cannot be empty")

    # ── item access ───────────────────────────────────────────────────────────

    def get_item(self, item_id: str, calories: int | None = None) -> dict:
        """Get a menu item by item_id."""
        items = self.menu.get(item_id, None)
        if not items:
            raise KeyError(f"Item with ID '{item_id}' not found")
        if len(items) == 1:
            return items[0]
        if len(items) > 1:
            for item in items:
                if calories and item.get("calories") == calories:
                    return item

    def get_by_category(self, category: str) -> list:
        """Get all items for a given meal category."""
        category_map = {
            'Entree':  self.entrees,
            'Side':    self.sides,
            'Drink':   self.drinks,
            'Dessert': self.desserts,
            'Add-on':  self.addons,
        }
        result = category_map.get(category)
        if result is None:
            raise ValueError(f"Unknown category: {category}. Must be one of {list(category_map.keys())}")
        return result
    
    def to_dict(self):
        """Convert restaurant data to JSON-serializable format."""
        return {
            'name': self.name,
            'entrees': self.entrees,
            'sides': self.sides,
            'drinks': self.drinks,
            'desserts': self.desserts,
            'addons': self.addons,
            'entree_combos': self.entree_combos
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Restaurant":
        # TODO: UPDATE FOR DB KEYS
        return cls(
            name = data['name'],
            menu = data,
            entrees = data.get('entrees', []),
            sides = data.get('sides', []),
            drinks = data.get('drinks', []),
            desserts = data.get('desserts', []),
            addons = data.get('addons', []),
            entree_combos = data.get('entree_combos', [])
        )

    # ── stats ─────────────────────────────────────────────────────────────────

    @property
    def item_count(self) -> int:
        return len(self.menu)

    @property
    def combo_count(self) -> int:
        return len(self.entree_combos)

    def summary(self) -> str:
        return (
            f"{self.name}: "
            f"{self.item_count} items  "
            f"({len(self.entrees)} entrees, "
            f"{len(self.sides)} sides, "
            f"{len(self.drinks)} drinks, "
            f"{len(self.desserts)} desserts, "
            f"{len(self.addons)} add-ons)  "
            f"{self.combo_count} entree combos"
        )