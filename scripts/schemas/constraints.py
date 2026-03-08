import math
from dataclasses import dataclass

@dataclass
class Constraints:
    _price: float = 14.00
    _calories: int = 800
    _protein: int = 20
    
    # Tolerances: not sure if these will change
    _price_tol_pct: float = 0.20
    _cal_tol_pct: float = 0.10
    _protein_tol_pct: float = 0.30

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if self._price <= 0:
            raise ValueError("Price must be positive")
        if self._calories <= 0:
            raise ValueError("Calories must be positive")
        if self._protein <= 0:
            raise ValueError("Protein must be positive")
        if not (0 < self._price_tol_pct < 1):
            raise ValueError("Price tolerance must be between 0 and 1")
        if not (0 < self._cal_tol_pct < 1):
            raise ValueError("Calorie tolerance must be between 0 and 1")
        if not (0 < self._protein_tol_pct < 1):
            raise ValueError("Protein tolerance must be between 0 and 1")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError(f"Unknown constraint field: {key}")
            setattr(self, key, value)
        self._validate()

    @property
    def price(self) -> float:
        return round(self._price * self._price_tol_pct, 2)

    @property
    def cal(self) -> int:
        return math.ceil(self._calories * self._cal_tol_pct)

    @property
    def protein(self) -> int:
        return math.ceil(self._protein * self._protein_tol_pct)

    def to_dict(self) -> dict:
        return {
            "price": self._price,
            "calories": self._calories,
            "protein": self._protein,
            "price_tol_pct": self._price_tol_pct,
            "cal_tol_pct": self._cal_tol_pct,
            "protein_tol_pct": self._protein_tol_pct,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Constraints":
        return cls(
            _price=data["price"],
            _calories=data["calories"],
            _protein=data["protein"],
            _price_tol_pct=data.get("price_tol_pct", 0.20),
            _cal_tol_pct=data.get("cal_tol_pct", 0.10),
            _protein_tol_pct=data.get("protein_tol_pct", 0.30),
        )