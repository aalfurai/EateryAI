import json
import uuid
from db import get_db_connection

def insert_meals_from_json(file_path):
    conn = get_db_connection()
    if not conn: 
        return
    cur = conn.cursor()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
            if isinstance(items, dict): items = [items]

        for item in items:
            # upserting restaurant
            # link restaurant_id to the menu_item
            cur.execute("""
                INSERT INTO restaurants (restaurant_id, restaurant_name, menu_card_image)
                VALUES (%s, %s, %s)
                ON CONFLICT (restaurant_name) DO UPDATE SET menu_card_image = EXCLUDED.menu_card_image
                RETURNING restaurant_id;
            """, (str(uuid.uuid4()), item['restaurant_name'], item['menu_card_image']))
            res_id = cur.fetchone()[0]

            # insert menu item
            cur.execute("""
                INSERT INTO menu_items (item_id, menu_item_id, restaurant_id, menu_item_name, category, price, golden_ratio, ai_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (item_id) DO NOTHING;
            """, (
                item['item_id'],
                item.get('menu_item_id', str(uuid.uuid4())),
                res_id,
                item['menu_item_name'],
                item['category'],
                item['price'],
                item['golden_ratio'],
                item['ai_description']
            ))

            # insert nutrition
            ni = item['nutrition_info']
            cur.execute("""
                INSERT INTO nutrition_info (item_id, serving_size, calories, cholesterol, sodium, total_carbohydrates, dietary_fiber, sugars, protein, potassium, total_fat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (item_id) DO NOTHING;
            """, (
                item['item_id'], ni['serving_size'], ni['calories'], ni['cholesterol'],
                ni['sodium'], ni['total_carbohydrates'], ni['dietary_fiber'],
                ni['sugars'], ni['protein'], ni['potassium'], ni['total_fat']
            ))

            # insert cuisines
            for cuisine in item.get('cuisine_type', []):
                cur.execute("""
                    INSERT INTO menu_item_cuisines (cuisine_type, item_id)
                    VALUES (%s, %s);
                """, (cuisine, item['item_id']))

        conn.commit()
        print("Data added to all tables")

    except Exception as e:
        conn.rollback()
        print(f"Rollback.\nError: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    insert_meals_from_json('data/restaurants.menu_item_variations.json')
