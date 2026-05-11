from dataclasses import dataclass

@dataclass
class Weights:
    price: float = 0.20
    #calories: float = 0.40
    cal_surplus: float = 0.40 # user's tolerance for more calores
    cal_deficit: float = 0.05 # user's tolerance for less calories
    protein: float = 0.40
    
    fiber: float = 0.0
    sugar: float = 0.0
    sodium: float = 0.0

    drink_cal: float = 0.0
    addon_cal: float = 0.0

    def __post_init__(self):
        self._validate()

    # NOTE: can add more validation
    def _validate(self):
        for field in ["price", "calories", "protein", "fiber", "sugar", "sodium", "drink_cal", "addon_cal"]:
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
            "cal_surplus": self.cal_surplus,
            "cal_deficit": self.cal_deficit,
            "protein": self.protein,
            "fiber": self.fiber,
            "sugar": self.sugar,
            "sodium": self.sodium,
            "drink_cal": self.drink_cal,
            "addon_cal": self.addon_cal,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Weights":
        return cls(
            price=data.get("price", 0.20),
            cal_deficit=data.get("cal_deficit", 0.40),
            cal_surplus=data.get("cal_surplus", 0.05),
            protein=data.get("protein", 0.40),
            fiber=data.get("fiber", 0.0),
            sugar=data.get("sugar", 0.0),
            sodium=data.get("sodium", 0.0),
            drink_cal=data.get("drink_cal", 0.0),
            addon_cal=data.get("addon_cal", 0.0),
        )