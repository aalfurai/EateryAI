from dataclasses import dataclass

@dataclass
class Meal:
    entree: dict
    sides: list[dict]
    drink: dict
    dessert: dict
    addons: list[dict]
    score: float

    def __post_init__(self):
        self.totalPrice = sum(item['price'] for item in [self.entree] + self.sides + [self.drink] + [self.dessert] + self.addons)
        self.totalCalories = sum(item['calories'] for item in [self.entree] + self.sides + [self.drink] + [self.dessert] + self.addons)
        self.totalProtein = sum(item['protein'] for item in [self.entree] + self.sides + [self.drink] + [self.dessert] + self.addons)

    def get_price(self):
        return self.totalPrice
    def get_calories(self):
        return self.totalCalories
    def get_protein(self):
        return self.totalProtein
    def get_score(self):
        return self.score