import json
import uuid
import time
from db import get_db_connection

def to_numeric(value, default=None):
    if value == '' or value is None:
        return default
    try:
        cleaned = str(value).replace('$', '').strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return default

def insert_meals_from_json(file_path):
    conn = get_db_connection()
    if not conn: 
        return
    cur = conn.cursor()
    start_time = time.time()
    last_print_time = start_time
    entries_added = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
            if isinstance(items, dict): items = [items]

        for item in items:
            current_time = time.time()
            if current_time - last_print_time >= 5:
                print(f"Progress: {entries_added} entries added...")
                last_print_time = current_time

            if to_numeric(item['price']) is None:
                continue

            cur.execute("""
                INSERT INTO restaurants (restaurant_id, restaurant_name, menu_card_image)
                VALUES (%s, %s, %s)
                ON CONFLICT (restaurant_name) DO UPDATE SET menu_card_image = EXCLUDED.menu_card_image
                RETURNING restaurant_id;
            """, (str(uuid.uuid4()), item['restaurant_name'], item['menu_card_image']))
            res_id = cur.fetchone()[0]

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
                to_numeric(item['price']),
                to_numeric(item['golden_ratio']),
                item['ai_description']
            ))

            ni = item['nutrition_info']
            cur.execute("""
                INSERT INTO nutrition_info (item_id, serving_size, calories, cholesterol, sodium, total_carbohydrates, dietary_fiber, sugars, protein, potassium, total_fat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (item_id) DO NOTHING;
            """, (
                item['item_id'],
                ni['serving_size'],
                to_numeric(ni['calories']),
                to_numeric(ni['cholesterol']),
                to_numeric(ni['sodium']),
                to_numeric(ni['total_carbohydrates']),
                to_numeric(ni['dietary_fiber']),
                to_numeric(ni['sugars']),
                to_numeric(ni['protein']),
                to_numeric(ni['potassium']),
                to_numeric(ni['total_fat'])
            ))

            for cuisine in item.get('cuisine_type', []):
                cur.execute("""
                    INSERT INTO menu_item_cuisines (cuisine_type, item_id)
                    VALUES (%s, %s);
                """, (cuisine, item['item_id']))

            entries_added += 1

        conn.commit()
        total_time = round(time.time() - start_time, 2)
        print(f"Data added to all tables in {total_time} sec.")

    except Exception as e:
        conn.rollback()
        print(f"Rollback.\nError:\n\t{e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    insert_meals_from_json('data/restaurants.menu_item_variations.json')