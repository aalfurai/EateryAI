import math
from dataclasses import dataclass

@dataclass
class Constraints:
    price: float = 14.00
    calories: int = 800
    protein: int = 20
    
    # Tolerances: not sure if these will change
    price_tol_pct: float = 0.20
    cal_sur_tol_pct: float = 0.10
    cal_def_tol_pct: float = 0.05
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
        if not ((0 < self.cal_sur_tol_pct < 1) and (0 < self.cal_def_tol_prct < 1)):
            raise ValueError("Calorie tolerance must be between 0 and 1")
        if not (0 < self.protein_tol_pct < 1):
            raise ValueError("Protein tolerance must be between 0 and 1")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError(f"Unknown constraint field: {key}")
            setattr(self, key, value)
        self._validate()

    @property
    def get_price(self) -> float:
        return round(self.price * self.price_tol_pct, 2)

    @property
    def get_calories(self) -> int:
        return math.ceil(self.calories * self.cal_sur_tol_pct)

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
            "cal_sur_tol_pct": self.cal_sur_tol_pct,
            "cal_def_tol_pct": self.cal_def_tol_pct,
            "protein_tol_pct": self.protein_tol_pct,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Constraints":
        return cls(
            price=data["price"],
            calories=data["calories"],
            protein=data["protein"],
            price_tol_pct=data.get("price_tol_pct", 0.20),
            cal_sur_tol_pct=data.get("cal_sur_tol_pct", 0.10),
            cal_def_tol_pct=data.get("cal_def_tol_prct", 0.05),
            protein_tol_pct=data.get("protein_tol_pct", 0.30),
        )