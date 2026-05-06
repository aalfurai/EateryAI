from dataclasses import dataclass, field

@dataclass
class Meal:
    item_ids:           list[int] = field(default_factory=list)
    Entree_ids:         list[int] = field(default_factory=list)
    Side_ids:           list[int] = field(default_factory=list)
    Drink_ids:          list[int] = field(default_factory=list)
    Addon_ids:          list[int] = field(default_factory=list)
    Dessert_ids:        list[int] = field(default_factory=list)
    total_price:        float = 0.0
    total_cal:          int = 0
    total_protein:      int = 0
    total_fiber:        int = 0
    total_sugars:       int = 0
    total_sodium:       int = 0
    total_cholesterol:  int = 0
    total_carbohydrates:int = 0
    total_potassium:    int = 0
    total_fat:          int = 0
    filled_categories:  set = field(default_factory=set)
    drink_cal:          int = 0
    addon_cal:          int = 0
    filled_categories:  set = field(default_factory=set)
    total_price:        float = 0.0
    golden_ratio:       float = 0.0

    def get_price(self):
        return self.total_price
    def get_calories(self):
        return self.total_cal
    def get_protein(self):
        return self.total_protein
    # def get_score(self):
    #     return self.score