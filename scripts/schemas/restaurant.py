from dataclasses import dataclass, field

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

    def get_item(self, idx: int) -> dict:
        """Get a menu item by index."""
        item = self.menu.get(idx)
        if item is None:
            raise KeyError(f"Item index {idx} not found in {self.name}")
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