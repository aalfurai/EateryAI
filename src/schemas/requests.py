from pydantic import BaseModel

class SessionRequest(BaseModel):
    user_id: str

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