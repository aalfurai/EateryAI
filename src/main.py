from fastapi import FastAPI, HTTPException
from api.menu import router as menu_router
from pydantic import BaseModel
from services.pipeline import PipelineService
from services.data import DataService
from schemas.user import User


app = FastAPI()
app.include_router(menu_router)
dataService = DataService(base_url="http://localhost:8000")  # NOTE: Update with actual backend URL
pipeline = PipelineService(data_service=dataService)

@app.get("/")
async def root():
    return {"message": "Welcome to Eatery"}

class RecommendRequest(BaseModel):
    user_id: str
    restaurant_name: str | None = None
    categories: list[str] = ["Entree", "Side", "Drink"]
    seed_id: str | None = None

@app.post("/recommend")
def recommend(req: RecommendRequest):
    return pipeline.recommend_from_seed(req.user_id, req.restaurant_name, req.seed_id)

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = User(user_id=user_id, name=f"Test User {user_id}")
    return user.to_dict()