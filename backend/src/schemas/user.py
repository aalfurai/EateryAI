from dataclasses import dataclass, field
from schemas.meal import Meal
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
    
    def strong_update(self, meal: Meal, update_strength=1.0):
        # LEARNING PARAMETERS
        # TODO bugfix, updates are inversed?
        learning_rate = 0.005*update_strength
        decay_constant = 0.001*update_strength #combats parameter drift

        price_deviation = (self.constraints.get_price-meal.get_price())/self.constraints.get_price
        calorie_sur = max(0, meal.get_calories()-self.constraints.get_calories)/self.constraints.get_calories
        calorie_def = max(0, -calorie_sur)/self.constraints.get_calories
        protein_deviation = (self.constraints.get_protein-meal.get_protein())/self.constraints.get_protein

        updated_price = -learning_rate*price_deviation + (1-learning_rate)*self.weights.price - decay_constant
        updated_cal_sur = -learning_rate*calorie_sur + (1-learning_rate)*self.weights.cal_surplus - decay_constant
        updated_cal_def = -learning_rate*calorie_def + (1-learning_rate)*self.weights.cal_deficit - decay_constant
        updated_protein = -learning_rate*protein_deviation + (1-learning_rate)*self.weights.protein - decay_constant
        print("ASDASDASDASDASD", updated_price, updated_cal_sur, updated_cal_def, updated_protein)

        updated_weights = {
            "price": updated_price,
            "cal_surplus": updated_cal_sur,
            "cal_deficit": updated_cal_def,
            "protein": updated_protein,
        }
        self.update_weights(**updated_weights)

    def weak_update(self, meal: Meal):
        self.strong_update(meal, update_strength=0.3)

    def reset_weights(self, profile="default"):
        # hard-coded user "profiles" that can act like preference learning starting points
        '''
        relative expected % diffs of each category
        price: + 20% is normal, $10 going to 12 is usually reasonable
        cal_surplus: + 10% is normal, 1000->1100 for people on a cut, 
                     + 25% is normal, 2000->2500 for people on a bulk
        cal_deficit: - 10% is normal, 1000->900 for people on a cut
                     - 8% is normal, 1500->1380 for people on a bulk
        protein: - 20% is normal, 30g -> 24g is reasonable for people
        '''
        if(profile=="bulking"):
            weights = {
                "price": 0.50,
                "cal_surplus": 0.15,
                "cal_deficit": 0.50,
                "protein": 0.15
            }
        elif(profile=="cutting"):
            weights = {
                "price": 0.50,
                "cal_surplus": 0.30,
                "cal_deficit": 0.15,
                "protein": 0.15
            }
        elif(profile=="budget"):
            weights = {
                "price": 0.7,
                "cal_surplus": 0.3,
                "cal_deficit": 0.3,
                "protein": 0.4
            }
        else: # (profile=="default")
            weights = {
                "price": 0.5,
                "cal_surplus": 0.40,
                "cal_deficit": 0.05,
                "protein": 0.40
            }
        self.update_weights(**weights)