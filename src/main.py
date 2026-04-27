import time
from fastapi import FastAPI, Depends, Request
from schemas.user import User
from schemas.requests import SessionRequest, RecommendRequest, ConstraintsRequest, WeightsRequest
from config.security import create_token, decode_token
from config.dependencies import pipeline, security, data_service


app = FastAPI()

@app.middleware("http")
async def timer(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    print(f"{request.method} {request.url.path} — {duration * 1000:.2f}ms")
    response.headers["X-Process-Time"] = f"{duration * 1000:.2f}ms"
    return response

@app.get("/")
def welcome():
    return {"message": "Welcome to the Eatery meal recommendation API!"}

@app.post("/")
def root(req: SessionRequest):
    user = pipeline.start_session(req.user_id)
    token = create_token(req.user_id)
    return {"token": token, "user": user.to_dict()}

@app.post("/recommend")
def recommend(req: RecommendRequest, credentials=Depends(security)):
    user_id = decode_token(credentials.credentials)  # NOTE: token is not currently used for anything beyond auth, but will be used to pull user preferences in the future
    user = data_service.load_user(user_id)
    return pipeline.recommend(user, req.restaurant_name, req.seed_id, req.categories)

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = User(user_id=user_id, name=f"Test User {user_id}")
    return user.to_dict()

@app.put("/user/constraints")
def update_constraints(req: ConstraintsRequest, credentials=Depends(security)):
    user_id = decode_token(credentials.credentials)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    user    = data_service.update_user_constraints(user_id, **updates)
    return user.to_dict()

@app.put("/user/weights")
def update_weights(req: WeightsRequest, credentials=Depends(security)):
    user_id = decode_token(credentials.credentials)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    user    = data_service.update_user_weights(user_id, **updates)
    return user.to_dict()