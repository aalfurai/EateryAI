from pydantic import BaseModel

class SessionRequest(BaseModel):
    user_id: str

class RecommendRequest(BaseModel):
    restaurant_name: str | None = None
    categories: set[str] = {"Entree", "Side", "Drink"}
    seed_id: str | None = None