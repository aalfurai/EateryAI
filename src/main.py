from fastapi import FastAPI, Depends
from schemas.user import User
from schemas.requests import SessionRequest, RecommendRequest
from config.security import create_token, decode_token
from config.dependencies import pipeline, security


app = FastAPI()

@app.post("/")
def root(req: SessionRequest):
    user = pipeline.start_session(req.user_id)
    token = create_token(req.user_id)
    return {"token": token, "user": user.to_dict()}

@app.post("/recommend")
def recommend(req: RecommendRequest, credentials=Depends(security)):
    decode_token(credentials.credentials)  # NOTE: token is not currently used for anything beyond auth, but could be used to pull user preferences in the future
    return pipeline.recommend_from_seed(req.restaurant_name, req.seed_id, req.categories)

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = User(user_id=user_id, name=f"Test User {user_id}")
    return user.to_dict()