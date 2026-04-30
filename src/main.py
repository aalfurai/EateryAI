import time
from fastapi import FastAPI, Depends, Request
from schemas.user import User
from schemas.requests import SessionRequest, RecommendRequest, ConstraintsRequest, WeightsRequest
from config.security import create_token, decode_token
from config.dependencies import pipeline, security, data_service

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from schemas.user import User
from schemas.restaurant import Restaurant
from schemas.constraints import Constraints
from schemas.weights import Weights
import solver.functions as solver
from services.data import DataService
from backend import queries
from backend.classes import NumRange
from db.db_connection import EateryDatabaseConnection


# ─────────────────────────────────────────────
# App init
# ─────────────────────────────────────────────

app = FastAPI(title="EatAI API", version="1.0.0")

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

# ─────────────────────────────────────────────
# In-memory stubs
# ─────────────────────────────────────────────

# user_id -> User
_users: dict[str, User] = {}

# user_id -> list of saved meal dicts
_saved_meals: dict[str, list] = {}


def _get_user(user_id: str) -> User:
    user = _users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return user


# ─────────────────────────────────────────────
# Request models
# ─────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    user_id: str

class RegisterRequest(BaseModel):
    user_id: str
    name: str
    constraints: Optional[dict] = None
    weights: Optional[dict] = None

class ConstraintsUpdateRequest(BaseModel):
    price: Optional[float] = None
    calories: Optional[int] = None
    protein: Optional[int] = None
    price_tol_pct: Optional[float] = None
    calories_tol_pct: Optional[float] = None
    protein_tol_pct: Optional[float] = None

class WeightsUpdateRequest(BaseModel):
    price: Optional[float] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    cheap: Optional[float] = None

class RecommendRequest(BaseModel):
    user_id: str
    restaurant_name: str
    seed_id: Optional[str] = None

class SaveMealRequest(BaseModel):
    meal: dict


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────


VALID_CATEGORIES = {"Entree", "Side", "Drink", "Dessert", "Add-On"}

def _resolve_restaurant_id(conn, restaurant_name: str) -> str:
    """Look up restaurant_id by name or raise 404."""
    rows = queries.find_restaurant_by_name(conn, restaurant_name)
    if not rows:
        raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_name}' not found")
    return rows[0]["restaurant_id"]

def _build_solver_restaurant(conn, restaurant_id: str, restaurant_name: str) -> Restaurant:
    """
    Load items from DB and assemble a Restaurant object with category lists
    and entree combos — everything the solver needs, with no DataService.
    """
    rows = queries.get_menu_items_for_solver(conn, restaurant_id)

    menu = {}
    entrees, sides, drinks, desserts, addons = [], [], [], [], []

    for idx, row in enumerate(rows):
        item = {
            "index":          idx,
            "item_id":        row["item_id"],
            "menu_item_name": row["menu_item_name"],
            "price":          float(row["price"]),
            "calories":       int(row["calories"] or 0),
            "protein":        int(row["protein"] or 0),
            "category":       row["category"],
        }
        menu[idx] = item
        match item["category"]:
            case "Entree":  entrees.append(item)
            case "Side":    sides.append(item)
            case "Drink":   drinks.append(item)
            case "Dessert": desserts.append(item)
            case "Add-On":  addons.append(item)

    entree_combos = DataService._calculate_entree_combos(entrees)

    return Restaurant(
        name=restaurant_name,
        menu=menu,
        entrees=entrees,
        sides=sides,
        drinks=drinks,
        desserts=desserts,
        addons=addons,
        entree_combos=entree_combos,
    )

def _serialize_meals(meals: list) -> list:
    """Make meal dicts JSON-safe (sets -> lists)."""
    result = []
    for meal in meals:
        m = dict(meal)
        if isinstance(m.get("filled_categories"), set):
            m["filled_categories"] = list(m["filled_categories"])
        result.append(m)
    return result


# ─────────────────────────────────────────────
# Root
# ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
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
    if req.user_id in _users:
        raise HTTPException(status_code=409, detail="User already exists")
    constraints = Constraints.from_dict(req.constraints) if req.constraints else Constraints()
    weights = Weights.from_dict(req.weights) if req.weights else Weights()
    user = User(user_id=req.user_id, name=req.name, constraints=constraints, weights=weights)
    _users[req.user_id] = user
    _saved_meals[req.user_id] = []
    return {"message": "User registered", "user": user.to_dict()}


@app.post("/auth/login", tags=["Auth"])
def login(req: LoginRequest):
    """
    Log in / auto-create a user. Corresponds to the Login screen.
    """
    if req.user_id not in _users:
        user = User(user_id=req.user_id, name=req.username)
        _users[req.user_id] = user
        _saved_meals[req.user_id] = []
    return {"message": "Login successful", "user": _users[req.user_id].to_dict()}


# ─────────────────────────────────────────────
# Users
# ─────────────────────────────────────────────

@app.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: str):
    """Return user profile. Corresponds to the Profile / @User screen."""
    return _get_user(user_id).to_dict()

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

@app.patch("/users/{user_id}/constraints", tags=["Users"])
def update_constraints(user_id: str, req: ConstraintsUpdateRequest):
    """
    Update nutritional / budget constraints.
    Corresponds to the Filters modal (Price, Calories, Protein sliders).
    """
    user = _get_user(user_id)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    try:
        user.update_constraints(**updates)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"message": "Constraints updated", "constraints": user.constraints.to_dict()}


@app.patch("/users/{user_id}/weights", tags=["Users"])
def update_weights(user_id: str, req: WeightsUpdateRequest):
    """Update solver weights (price / calories / protein / cheap)."""
    user = _get_user(user_id)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    try:
        user.update_weights(**updates)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"message": "Weights updated", "weights": user.weights.to_dict()}


# ─────────────────────────────────────────────
# Saved Meals
# ─────────────────────────────────────────────

@app.get("/users/{user_id}/saved", tags=["Saved Meals"])
def get_saved_meals(user_id: str):
    """
    Return all saved meals. Corresponds to the Saved Meals list on the Profile screen.
    """
    _get_user(user_id)
    return {"saved_meals": _saved_meals.get(user_id, [])}


@app.post("/users/{user_id}/saved", tags=["Saved Meals"])
def save_meal(user_id: str, req: SaveMealRequest):
    """Save a recommended meal to the user's profile."""
    _get_user(user_id)
    _saved_meals.setdefault(user_id, []).append(req.meal)
    return {"message": "Meal saved", "saved_count": len(_saved_meals[user_id])}


@app.delete("/users/{user_id}/saved/{meal_index}", tags=["Saved Meals"])
def delete_saved_meal(user_id: str, meal_index: int):
    """Remove a saved meal by index."""
    _get_user(user_id)
    meals = _saved_meals.get(user_id, [])
    if meal_index < 0 or meal_index >= len(meals):
        raise HTTPException(status_code=404, detail="Saved meal not found")
    removed = meals.pop(meal_index)
    return {"message": "Meal removed", "removed": removed}


# ─────────────────────────────────────────────
# Restaurants
# ─────────────────────────────────────────────

@app.get("/restaurants", tags=["Restaurants"])
def all_restaurants():
    """
    List all restaurants.
    Corresponds to the 'Build Meal by Restaurant' browse screen.
    """
    with EateryDatabaseConnection() as conn:
        return queries.get_all_restaurants(conn)


@app.get("/restaurants/search", tags=["Restaurants"])
def search_restaurants(name: str = Query(..., min_length=1)):
    """Case-insensitive partial-match restaurant search."""
    with EateryDatabaseConnection() as conn:
        results = queries.find_restaurant_by_name(conn, name)
    if not results:
        raise HTTPException(status_code=404, detail=f"No restaurants matching '{name}'")
    return results


# ─────────────────────────────────────────────
# Menu
# ─────────────────────────────────────────────

@app.get("/menu/{restaurant}", tags=["Menu"])
def get_menu(restaurant: str):
    """
    Full menu for a restaurant (all categories + nutrition).
    Corresponds to the restaurant card tap on the Browse screen.
    """
    with EateryDatabaseConnection() as conn:
        restaurant_id = _resolve_restaurant_id(conn, restaurant)
        items = queries.get_menu_items_by_restaurant(conn, restaurant_id)
    return {"restaurant": restaurant, "items": items}


@app.get("/menu/{restaurant}/category/{category}", tags=["Menu"])
def get_menu_by_category(restaurant: str, category: str):
    """
    Menu items filtered by category (Entree | Side | Drink | Dessert | Add-On).
    Corresponds to the category tabs on the For You / Browse screens.
    """
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=422,
            detail=f"Category must be one of {sorted(VALID_CATEGORIES)}"
        )
    with EateryDatabaseConnection() as conn:
        restaurant_id = _resolve_restaurant_id(conn, restaurant)
        items = queries.get_menu_items_by_category(conn, restaurant_id, category)
    return {"restaurant": restaurant, "category": category, "items": items}


@app.get("/menu/{restaurant}/{item_id}", tags=["Menu"])
def get_restaurant_item(restaurant: str, item_id: str):
    """
    Single menu item detail view.
    Corresponds to the Menu Item Name screen
    (picture, Meal Description, Nutrition Information).
    """
    with EateryDatabaseConnection() as conn:
        _resolve_restaurant_id(conn, restaurant)  # 404 if restaurant not found
        item = queries.get_menu_item_by_id(conn, item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item '{item_id}' not found in '{restaurant}'"
        )
    return item


# ─────────────────────────────────────────────
# Search
# ─────────────────────────────────────────────

@app.get("/search", tags=["Search"])
def search_items(
    q: Optional[str] = Query(None, description="Item name (partial match)"),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    calories_min: Optional[int] = Query(None),
    calories_max: Optional[int] = Query(None),
    protein_min: Optional[int] = Query(None),
    protein_max: Optional[int] = Query(None),
):
    """
    Cross-restaurant item search with optional filters.
    Corresponds to the search / filter flow from the nav bar.
    """
    price_range    = NumRange(price_min, price_max)       if (price_min    is not None or price_max    is not None) else None
    calories_range = NumRange(calories_min, calories_max) if (calories_min is not None or calories_max is not None) else None
    protein_range  = NumRange(protein_min, protein_max)   if (protein_min  is not None or protein_max  is not None) else None

    with EateryDatabaseConnection() as conn:
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
def recommend(req: RecommendRequest):
    """
    Run the meal-building pipeline for a user.

    • seed_id provided → build meal anchored to that item
      (tapping 'Build Full Meal' on the item detail screen).
    • No seed_id       → build top combos for the restaurant freely.

    Returns up to 3 ranked meal combos.
    """
    user = _get_user(req.user_id)

    with EateryDatabaseConnection() as conn:
        restaurant_id = _resolve_restaurant_id(conn, req.restaurant_name)
        restaurant = _build_solver_restaurant(conn, restaurant_id, req.restaurant_name)

    anchor = None
    if req.seed_id:
        anchor = next(
            (item for item in restaurant.menu.values() if item["item_id"] == req.seed_id),
            None
        )
        if not anchor:
            raise HTTPException(
                status_code=404,
                detail=f"Item '{req.seed_id}' not found in '{req.restaurant_name}'"
            )

    try:
        meals = solver.build_meal(
            user=user,
            seed_id=anchor["index"] if anchor else None,
            required_categories={"Entree", "Side", "Drink"},
            restaurant=restaurant,
            entree_combos=restaurant.entree_combos,
            sides=restaurant.sides,
            drinks=restaurant.drinks,
            desserts=restaurant.desserts,
            addons=restaurant.addons,
            build_full=bool(anchor),
        )
        ranked = solver.score_and_rank_meals(user, meals)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

    return {"recommendations": _serialize_meals(ranked[:3])}


@app.post("/recommend/for-you", tags=["Recommend"])
def for_you_feed(user_id: str, limit: int = Query(default=10, le=50)):
    """
    Personalised 'For You' feed across all restaurants.
    Returns the top recommendation per restaurant up to `limit` results.
    Corresponds to the main For You tab on the home screen.
    """
    user = _get_user(user_id)

    with EateryDatabaseConnection() as conn:
        restaurants = queries.get_all_restaurants(conn)

        feed = []
        for r in restaurants:
            if len(feed) >= limit:
                break
            try:
                restaurant = _build_solver_restaurant(conn, r["restaurant_id"], r["restaurant_name"])
                meals = solver.build_meal(
                    user=user,
                    seed_id=None,
                    required_categories={"Entree", "Side", "Drink"},
                    restaurant=restaurant,
                    entree_combos=restaurant.entree_combos,
                    sides=restaurant.sides,
                    drinks=restaurant.drinks,
                    desserts=restaurant.desserts,
                    addons=restaurant.addons,
                    build_full=False,
                )
                ranked = solver.score_and_rank_meals(user, meals)
                if ranked:
                    top = dict(ranked[0])
                    if isinstance(top.get("filled_categories"), set):
                        top["filled_categories"] = list(top["filled_categories"])
                    top["restaurant_name"] = r["restaurant_name"]
                    feed.append(top)
            except Exception:
                continue  # skip restaurants with missing/incomplete data

    return {"feed": feed, "count": len(feed)}
