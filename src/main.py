from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from services.pipeline import PipelineService
from services.data import DataService
from schemas.user import User
from dependencies import get_all_menus


app = FastAPI()
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

@app.get("/menu")
def menu():
    return get_all_menus()

@app.get("/menu/{restaurant}/{item_id}")
def menu(restaurant: str, item_id: int):
    restaurant_data = dataService.load_restaurant(restaurant)
    try:
        item = restaurant_data.get_item(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item ID '{item_id}' not found in restaurant '{restaurant}'")
    return item

@app.get("/menu/{restaurant}")
def menu(restaurant: str):
    restaurant_data = dataService.load_restaurant(restaurant)
    return restaurant_data.to_dict()