from dataclasses import dataclass, field
from schemas.constraints import Constraints
from schemas.weights import Weights

@dataclass
class User:
    user_id: str
    name: str
    constraints: Constraints = field(default_factory=Constraints)
    weights: Weights = field(default_factory=Weights)

    def __post_init__(self):
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")

    def update_constraints(self, **kwargs):
        self.constraints.update(**kwargs)

    def update_weights(self, **kwargs):
        self.weights.update(**kwargs)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "constraints": self.constraints.to_dict(),
            "weights": self.weights.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        # TODO: UPDATE FOR DB KEYS
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            constraints=Constraints.from_dict(data["constraints"]),
            weights=Weights.from_dict(data["weights"]),
        )
    
    def strong_update(self, meal, update_strength=1.0):
        # LEARNING PARAMETERS
        learning_rate = 0.005*update_strength
        # TODO integrate decay parameter AND/OR have a "RESET" function
        decay_constant = 0.001*update_strength #combats parameter drift

        price_deviation = self.constraints.get_price()-meal.get_price()
        calorie_sur = min(0, meal.get_calories()-self.constraints.get_calories())
        calorie_def = min(0, -calorie_sur)
        protein_deviation = self.constraints.get_protein()-meal.get_protein

        updated_price = learning_rate*price_deviation + (1-learning_rate)*self.weights.price - decay_constant
        updated_cal_sur = learning_rate*calorie_sur + (1-learning_rate)*self.weights.cal_surplus - decay_constant
        updated_cal_def = learning_rate*calorie_def + (1-learning_rate)*self.weights.cal_deficit - decay_constant
        updated_protein = learning_rate*protein_deviation + (1-learning_rate)*self.weights.protein - decay_constant

        updated_weights = {
            "price": updated_price,
            "cal_surplus": updated_cal_sur,
            "cal_deficit": updated_cal_def,
            "protein": updated_protein,
        }
        self.update_weights(**updated_weights)

    def weak_update(self, meal):
        self.strong_update(meal, update_strength=0.3)

    def reset_weights(self, profile="default"):
        # hard-coded user "profiles" that can act like preference learning starting points
        if(profile=="bulking"):
            weights = {
                "price": 0.30,
                "cal_surplus": 0.50,
                "cal_deficit": 0.10,
                "protein": 0.10
            }
        elif(profile=="cutting"):
            weights = {
                "price": 0.30,
                "cal_surplus": 0.10,
                "cal_deficit": 0.40,
                "protein": 0.15
            }
        elif(profile=="budget"):
            weights = {
                "price": 0.1,
                "cal_surplus": 0.5,
                "cal_deficit": 0.4,
                "protein": 0.3
            }
        else:
            weights = {
                "price": 0.20,
                "cal_surplus": 0.40,
                "cal_deficit": 0.05,
                "protein": 0.40
            }
        self.update_weights(**weights)