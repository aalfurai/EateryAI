from dataclasses import dataclass

@dataclass
class Weights:
    price: float = 0.20
    calories: float = 0.40
    protein: float = 0.40
    cheap: float = 0.20

    def __post_init__(self):
        self._validate()

    def _validate(self):
        for field in ["price", "calories", "protein", "cheap"]:
            value = getattr(self, field)
            if not (0 <= value <= 1):
                raise ValueError(f"{field} weight must be between 0 and 1")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError(f"Unknown weight field: {key}")
            setattr(self, key, value)
        self._validate()

    def to_dict(self) -> dict:
        return {
            "price": self.price,
            "calories": self.calories,
            "protein": self.protein,
            "cheap": self.cheap,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Weights":
        return cls(
            price=data.get("price", 0.20),
            calories=data.get("calories", 0.40),
            protein=data.get("protein", 0.40),
        )