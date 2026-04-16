import psycopg2.extras

# CRUD functions
# notes: using RealDictCursor for the purpose of making result queries easier to navigate

# Create
# Need to add more "create" functions

def add_new_restaurant(conn, restaurant_data: dict):
    """Inserts a new restaurant record."""
    with conn.cursor() as cur:
        query = """
            INSERT INTO restaurants (restaurant_id, restaurant_name, menu_card_image)
            VALUES (%s, %s, %s)
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
        cur.execute("SELECT * FROM restaurants")
        return cur.fetchall()

def find_restaurant_by_name(conn, name: str):
    """Searches for a restaurant using a case-insensitive partial match."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        pass

def get_menu_items_by_restaurant(conn, restaurant_id: int):
    """Fetches all food items for a specific restaurant ID."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        pass


# Update

""" Not necessary for now"""

# Delete

def delete_restaurant(conn, restaurant_id: int):
    """Removes restaurant."""
    with conn.cursor() as cur:
        pass
    conn.commit()

def delete_item_completely(conn, item_id: str):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM nutrition_info WHERE item_id = %s", (item_id,))
        cur.execute("DELETE FROM menu_items WHERE item_id = %s", (item_id,))
    conn.commit()