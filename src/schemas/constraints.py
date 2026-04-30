import math
from dataclasses import dataclass

@dataclass
class Constraints:
    price: float = 14.00
    calories: int = 800
    protein: int = 20
    
    # Tolerances: not sure if these will change
    price_tol_pct: float = 0.20
    calories_tol_pct: float = 0.10
    protein_tol_pct: float = 0.30

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if self.price <= 0:
            raise ValueError("Price must be positive")
        if self.calories <= 0:
            raise ValueError("Calories must be positive")
        if self.protein <= 0:
            raise ValueError("Protein must be positive")
        if not (0 < self.price_tol_pct < 1):
            raise ValueError("Price tolerance must be between 0 and 1")
        if not (0 < self.calories_tol_pct < 1):
            raise ValueError("Calorie tolerance must be between 0 and 1")
        if not (0 < self.protein_tol_pct < 1):
            raise ValueError("Protein tolerance must be between 0 and 1")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            print(f"Updating: {key} to {value}")
            if not hasattr(self, key):
                raise ValueError(f"Unknown constraint field: {key}")
            setattr(self, key, value)
        self._validate()

    @property
    def get_price(self) -> float:
        return round(self.price * self.price_tol_pct, 2)

    @property
    def get_calories(self) -> int:
        return math.ceil(self.calories * self.calories_tol_pct)

    @property
    def get_protein(self) -> int:
        return math.ceil(self.protein * self.protein_tol_pct)

    @classmethod
    def to_dict(self) -> dict:
        return {
            "price": self.price,
            "calories": self.calories,
            "protein": self.protein,
            "price_tol_pct": self.price_tol_pct,
            "calories_tol_pct": self.calories_tol_pct,
            "protein_tol_pct": self.protein_tol_pct,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Constraints":
        return cls(
            price=data["price"],
            calories=data["calories"],
            protein=data["protein"],
            price_tol_pct=data.get("price_tol_pct", 0.20),
            calories_tol_pct=data.get("calories_tol_pct", 0.10),
            protein_tol_pct=data.get("protein_tol_pct", 0.30),
        )