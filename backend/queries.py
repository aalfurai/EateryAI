import psycopg2.extras
import query_helpers

# CRUD functions
# notes: using RealDictCursor for the purpose of making result queries easier to navigate

# Create
# Need to add more "create" functions

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


# Read

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
    
def get_menu_items_by_restaurant(conn, restaurant_id: int):
    """Fetches all food items for a specific restaurant ID."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM menu_items WHERE restaurant_id = %s;", (restaurant_id,))
        return cur.fetchall()
    
def find_food_item(conn, food_item: str):
    """
        Finds a particular food item across all restaurants using a case-insensitive search
        including mix-case (ILIKE).
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = """
            SELECT
                r.restaurant_name,
                m.menu_item_name,
                m.category,
                m.price,
                m.golden_ratio
            FROM menu_items m
            JOIN restaurants r ON m.restaurant_id = r.restaurant_id
            WHERE m.menu_item_name ILIKE %s;
        """
        cur.execute(query, (f"%{food_item}%",))
        return cur.fetchall()

# Update

""" Not necessary for now"""

# Delete

def delete_restaurant(conn, restaurant_id: int):
    """Removes restaurant."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM restaurants WHERE restaurant_id = %s;", (restaurant_id,))    
        conn.commit()
    
    conn.commit()

def delete_item_completely(conn, item_id: str):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM menu_items WHERE item_id = %s;", (item_id,))
    conn.commit()