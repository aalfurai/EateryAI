import time
from fastapi import FastAPI, Depends, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from schemas.user import User
from schemas.requests import RecommendRequest, ConstraintsRequest, WeightsRequest, SaveMealRequest, LoginRequest, RegisterRequest
from config.security import create_token, decode_token
from config.dependencies import pipeline, security, data_service
from config.db import init_pool, get_db, db_pool
from backend import queries
from backend.classes import NumRange
from contextlib import asynccontextmanager


# ─────────────────────────────────────────────
# App init
# ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    yield
    db_pool.closeall()

app = FastAPI(title="EatAI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http:localhost:3000"], #NOTE: Add frontend url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def timer(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{duration * 1000:.2f}ms"
    return response


# ─────────────────────────────────────────────
# Root
# ─────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to EatAI", "status": "ok"}


# ─────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────

@app.post("/auth/register", tags=["Auth"])
def register(req: RegisterRequest):
    """
    Create a new user. Corresponds to the Welcome / Get Started screen.
    """
    if data_service.check_user_exists(req.user_id):
        raise HTTPException(status_code=409, detail="User already exists")
    user = User(user_id=req.user_id, name=req.name, constraints=req.constraints, weights=req.weights)
    data_service.add_user(user)

    token = create_token(req.user_id)
    return {"message": "User registered", "token": token,  "user": user.to_dict()}


@app.post("/auth/login", tags=["Auth"])
def login(req: LoginRequest):
    """
    Log in / auto-create a user. Corresponds to the Login screen.
    """
    if not data_service.check_user_exists(req.user_id):
        user = User(user_id=req.user_id, name=req.username)
        data_service.add_user(user)
    
    token = create_token(req.user_id)
    return {"message": "Login successful", "token": token, "user": data_service.load_user(req.user_id).to_dict()}


# ─────────────────────────────────────────────
# Users NOTE: MIGHT NEED TO CHANGE USER TO UPDATE IN DATA SERVICE FOR DB UPDATE
# ─────────────────────────────────────────────

@app.get("/user/me", tags=["Users"])
def get_user(credentials=Depends(security)):
    """Return user profile. Corresponds to the Profile / @User screen."""
    user_id = decode_token(credentials.credentials)
    return data_service.load_user(user_id).to_dict()

@app.patch("/user/constraints", tags=["Users"])
def update_constraints(req: ConstraintsRequest, credentials=Depends(security)):
    """
    Update nutritional / budget constraints.
    Corresponds to the Filters modal (Price, Calories, Protein sliders).
    """
    user_id = decode_token(credentials.credentials)
    user = data_service.load_user(user_id)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    try:
        user.update_constraints(**updates)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"message": "Constraints updated", "constraints": user.constraints.to_dict()}

@app.put("/user/weights", tags=["Users"])
def update_weights(req: WeightsRequest, credentials=Depends(security)):
    """
    Update nutritional / budget constraints.
    Corresponds to the Filters modal (Price, Calories, Protein sliders).
    """
    user_id = decode_token(credentials.credentials)
    user = data_service.load_user(user_id)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    try:
        user.update_weights(**updates)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"message": "Weights updated", "weights": user.weights.to_dict()}


# ─────────────────────────────────────────────
# Saved Meals
# ─────────────────────────────────────────────

@app.get("/users/saved", tags=["Saved Meals"])
def get_saved_meals(credentials=Depends(security)):
    """
    Return all saved meals. Corresponds to the Saved Meals list on the Profile screen.
    """
    user_id = decode_token(credentials.credentials)
    return {"saved_meals": data_service.get_saved_meals(user_id)}


@app.post("/users/saved", tags=["Saved Meals"])
def save_meal(req: SaveMealRequest, credentials=Depends(security)):
    """Save a recommended meal to the user's profile."""
    user_id = decode_token(credentials.credentials)
    count = data_service.save_meal(user_id, req.meal)
    return {"message": "Meal saved", "saved_count": count}


@app.delete("/users/saved/{meal_index}", tags=["Saved Meals"])
def delete_saved_meal(meal_index: int, credentials=Depends(security)):
    """Remove a saved meal by index."""
    user_id = decode_token(credentials.credentials)
    removed = data_service.delete_saved_meal(user_id, meal_index)
    return {"message": "Meal removed", "removed": removed}


# ─────────────────────────────────────────────
# Restaurants
# ─────────────────────────────────────────────

@app.get("/restaurants", tags=["Restaurants"])
def all_restaurants(conn=Depends(get_db)):
    """
    List all restaurants.
    Corresponds to the 'Build Meal by Restaurant' browse screen.
    """
    return queries.get_all_restaurants(conn)


@app.get("/restaurants/search", tags=["Restaurants"])
def search_restaurants(name: str = Query(..., min_length=1), conn=Depends(get_db)):
    """Case-insensitive partial-match restaurant search."""
    results = queries.find_restaurant_by_name(conn, name)
    if not results:
        raise HTTPException(status_code=404, detail=f"No restaurants matching '{name}'")
    return results


# ─────────────────────────────────────────────
# Menu
# ─────────────────────────────────────────────

@app.get("/menu/{restaurant}", tags=["Menu"])
def get_menu(restaurant: str, conn=Depends(get_db)):
    """
    Full menu for a restaurant (all categories + nutrition).
    Corresponds to the restaurant card tap on the Browse screen.
    """
    restaurant_id, restaurant_name = data_service._resolve_restaurant_id(conn, restaurant)
    items = queries.get_menu_items_by_restaurant(conn, restaurant_id)
    return {"restaurant": restaurant_name, "items": items}

@app.get("/menu/{restaurant}/category/{category}", tags=["Menu"])
def get_menu_by_category(restaurant: str, category: str, conn=Depends(get_db)):
    """
    Menu items filtered by category (Entree | Side | Drink | Dessert | Add-On).
    Corresponds to the category tabs on the For You / Browse screens.
    """
    if category not in {"Entree", "Side", "Drink", "Dessert", "Add-On"}:
        raise HTTPException(
            status_code=422,
            detail="Category must be one of (Entree, Side, Drink, Dessert, Add-On)"
        )
    restaurant_id, _ = data_service._resolve_restaurant_id(conn, restaurant)
    items = queries.get_menu_items_by_category(conn, restaurant_id, category)
    return {"restaurant": restaurant, "category": category, "items": items}

@app.get("/menu/{restaurant}/{item_id}", tags=["Menu"])
def get_restaurant_item(restaurant_name: str, item_id: int, conn=Depends(get_db)):
    """
    Single menu item detail view.
    Corresponds to the Menu Item Name screen
    (picture, Meal Description, Nutrition Information).
    """
    restaurant = data_service.load_restaurant(conn, restaurant_name)
    item = restaurant.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item '{item_id}' not found in '{restaurant.name}'"
        )
    return item


# ─────────────────────────────────────────────
# Search
# ─────────────────────────────────────────────

@app.get("/search", tags=["Search"])
def search_items(
    q: str | None = Query(None, description="Item name (partial match)"),
    price_min: float | None = Query(None),
    price_max: float | None = Query(None),
    calories_min: int | None = Query(None),
    calories_max: int | None = Query(None),
    protein_min: int | None = Query(None),
    protein_max: int | None = Query(None),
    conn=Depends(get_db),
):
    """
    Cross-restaurant item search with optional filters.
    Corresponds to the search / filter flow from the nav bar.
    """
    price_range    = NumRange(price_min, price_max)       if (price_min    is not None or price_max    is not None) else None
    calories_range = NumRange(calories_min, calories_max) if (calories_min is not None or calories_max is not None) else None
    protein_range  = NumRange(protein_min, protein_max)   if (protein_min  is not None or protein_max  is not None) else None

    results = queries.find_food_item(
        conn,
        food_item=q or "",
        price=price_range,
        calories=calories_range,
        protein=protein_range,
    )
    return results


# ─────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────

@app.post("/recommend", tags=["Recommend"])
def recommend(req: RecommendRequest, credentials=Depends(security), conn=Depends(get_db)):
    """
    Run the meal-building pipeline for a user.

    • seed_id provided → build meal anchored to that item
      (tapping 'Build Full Meal' on the item detail screen).
    • No seed_id       → build top combos for the restaurant freely.

    Returns up to 3 ranked meal combos.
    """
    user_id = decode_token(credentials.credentials)
    user = data_service.load_user(user_id)
    return {"user": user.to_dict(), "recommendations": pipeline.recommend(conn, user, req.restaurant_name, req.seed_id, req.categories)}

# TODO: reimplement to recommend seed items only
# @app.post("/recommend/for-you", tags=["Recommend"])
# def for_you_feed(user_id: str, limit: int = Query(default=10, le=50), credentials=Depends(security), conn=Depends(get_db)):
#     """
#     Personalised 'For You' feed across all restaurants.
#     Returns the top recommendation per restaurant up to `limit` results.
#     Corresponds to the main For You tab on the home screen.
#     """
#     user_id = decode_token(credentials.credentials)
#     user = data_service.load_user(user_id)
    
#     restaurants = queries.get_all_restaurants(conn)

#     feed = []
#     for r in restaurants:
#         if len(feed) >= limit:
#             break
#         try:
#             restaurant = _build_solver_restaurant(conn, r["restaurant_id"], r["restaurant_name"])
#             meals = solver.build_meal(
#                 user=user,
#                 seed_id=None,
#                 required_categories={"Entree", "Side", "Drink"},
#                 restaurant=restaurant,
#                 entree_combos=restaurant.entree_combos,
#                 sides=restaurant.sides,
#                 drinks=restaurant.drinks,
#                 desserts=restaurant.desserts,
#                 addons=restaurant.addons,
#                 build_full=False,
#             )
#             ranked = solver.score_and_rank_meals(user, meals)
#             if ranked:
#                 top = dict(ranked[0])
#                 if isinstance(top.get("filled_categories"), set):
#                     top["filled_categories"] = list(top["filled_categories"])
#                 top["restaurant_name"] = r["restaurant_name"]
#                 feed.append(top)
#         except Exception:
#             continue  # skip restaurants with missing/incomplete data

#     return {"feed": feed, "count": len(feed)}
