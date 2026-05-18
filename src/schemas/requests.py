from pydantic import BaseModel
from schemas.constraints import Constraints
from schemas.weights import Weights
from schemas.meal import Meal
    
class LoginRequest(BaseModel):
    username: str
    user_id: str

class RegisterRequest(BaseModel):
    user_id: str
    name: str
    constraints: Constraints | None = None
    weights: Weights | None = None

class RecommendRequest(BaseModel):
    restaurant_name: str | None = None
    categories: set[str] = {"Entree", "Side", "Drink"}
    seed_id: str | None = None

class ConstraintsRequest(BaseModel):
    price: float | None = None
    calories: int | None = None
    protein: int | None = None
    price_tol_pct: float | None = None
    calories_tol_pct: float | None = None
    protein_tol_pct: float | None = None

class WeightsRequest(BaseModel):
    price: float | None = None
    calories: float | None = None
    protein: float | None = None
    fiber: float | None = None
    sugar: float | None = None
    sodium: float | None = None
    drink_cal: float | None = None
    addon_cal: float | None = None

class SaveMealRequest(BaseModel):
    meal: Meal