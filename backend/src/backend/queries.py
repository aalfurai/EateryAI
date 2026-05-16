import psycopg2.extras
import backend.query_helpers as query_helpers
from backend.classes import NumRange

# CRUD functions
# notes: using RealDictCursor for the purpose of making result queries easier to navigate

# ─────────────────────────────────────────────
# Create
# ─────────────────────────────────────────────

def add_new_restaurant(conn, restaurant_data: dict):
    """Inserts a new restaurant record."""
    with conn.cursor() as cur:
        query = """
            INSERT INTO restaurants (restaurant_id, restaurant_name, menu_card_image)
            VALUES (%s, %s, %s);
        """
        cur.execute(query, (
            restaurant_data["restaurant_id"], 
            restaurant_data["restaurant_name"], 
            restaurant_data["menu_card_image"]
        ))
    conn.commit()


# ─────────────────────────────────────────────
# Read — Restaurants
# ─────────────────────────────────────────────

def get_all_restaurants(conn):
    """Returns all restaurants."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM restaurants;")
        return cur.fetchall()

def find_restaurant_by_name(conn, name: str):
    """Searches for a restaurant using a case-insensitive partial match."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM restaurants WHERE restaurant_name ILIKE %s;", (f"%{name}%",))
        return cur.fetchall()


# ─────────────────────────────────────────────
# Read — Menu Items
# ─────────────────────────────────────────────

def get_menu_items_by_restaurant(conn, restaurant_id: str):
    """
    Fetches all menu items for a restaurant joined with nutrition info.
    Returns a list of dicts.
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT
                m.item_id,
                m.menu_item_name,
                m.category,
                m.price,
                m.golden_ratio,
                m.ai_description,
                n.calories,
                n.protein,
                n.total_fat,
                n.total_carbohydrates,
                n.sodium,
                n.serving_size
            FROM menu_items m
            JOIN nutrition_info n ON m.item_id = n.item_id
            WHERE m.restaurant_id = %s
            ORDER BY m.category, m.menu_item_name;
        """, (restaurant_id,))
        return cur.fetchall()

def get_menu_item_by_id(conn, item_id: str):
    """
    Fetches a single menu item by item_id with full nutrition info.
    Corresponds to the item detail screen.
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT
                m.item_id,
                m.menu_item_name,
                m.category,
                m.price,
                m.golden_ratio,
                m.ai_description,
                r.restaurant_name,
                r.menu_card_image,
                n.calories,
                n.protein,
                n.total_fat,
                n.total_carbohydrates,
                n.dietary_fiber,
                n.sugars,
                n.sodium,
                n.cholesterol,
                n.potassium,
                n.serving_size
            FROM menu_items m
            JOIN restaurants r ON m.restaurant_id = r.restaurant_id
            JOIN nutrition_info n ON m.item_id = n.item_id
            WHERE m.item_id = %s;
        """, (item_id,))
        return cur.fetchone()

def get_menu_items_by_category(conn, restaurant_id: str, category: str):
    """
    Fetches menu items for a restaurant filtered by meal category
    (Entree | Side | Drink | Dessert | Add-On).
    Corresponds to the category tabs on the For You / Browse screens.
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT
                m.item_id,
                m.menu_item_name,
                m.category,
                m.price,
                m.golden_ratio,
                m.ai_description,
                n.calories,
                n.protein,
                n.serving_size
            FROM menu_items m
            JOIN nutrition_info n ON m.item_id = n.item_id
            WHERE m.restaurant_id = %s
              AND m.category = %s
            ORDER BY m.menu_item_name;
        """, (restaurant_id, category))
        return cur.fetchall()

def get_menu_items_for_solver(conn, restaurant_id: str):
    """
    Fetches the minimal fields the solver needs:
    item_id, name, category, price, calories, protein, dietary fiber, sugar, sodium, cholesterol, carbohydrates, potassium, total fat, and serving size.
    Used by the recommend pipeline in place of loading from JSON.
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT
                m.item_id,
                m.menu_item_name,
                m.category,
                m.price,
                n.calories,
                n.protein,
                n.dietary_fiber,
                n.sugars,
                n.sodium,
                n.cholesterol,
                n.total_carbohydrates,
                n.potassium,
                n.total_fat,
                n.serving_size
            FROM menu_items m
            JOIN nutrition_info n ON m.item_id = n.item_id
            WHERE m.restaurant_id = %s;
        """, (restaurant_id,))
        return cur.fetchall()


# ─────────────────────────────────────────────
# Read — Cross-restaurant search
# ─────────────────────────────────────────────

def find_food_item(conn, food_item: str,
                   price: NumRange = None, calories: NumRange = None, protein: NumRange = None):
    """
    Finds menu items across all restaurants using a case-insensitive name
    search with optional price / calorie / protein range filters.
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = """
            SELECT
                r.restaurant_name,
                m.item_id,
                m.menu_item_name,
                m.category,
                m.price,
                m.golden_ratio,
                n.calories,
                n.protein
            FROM menu_items m
            JOIN restaurants r ON m.restaurant_id = r.restaurant_id
            JOIN nutrition_info n ON m.item_id = n.item_id
            WHERE 1=1
        """
        final_query, selectors = query_helpers.query_selector_for_item(
            query, food_item, price, calories, protein
        )
        cur.execute(final_query, selectors)
        return cur.fetchall()


# ─────────────────────────────────────────────
# Delete
# ─────────────────────────────────────────────

def delete_restaurant(conn, restaurant_id: int):
    """Removes a restaurant."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM restaurants WHERE restaurant_id = %s;", (restaurant_id,))
    conn.commit()

def delete_item_completely(conn, item_id: str):
    """Removes a menu item and its related rows (relies on DB cascade)."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM menu_items WHERE item_id = %s;", (item_id,))
    conn.commit()