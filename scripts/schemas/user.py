from dataclasses import dataclass, field
from scripts.schemas.constraints import Constraints
from scripts.schemas.weights import Weights

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