import src.db.db_connection as dbc
from datetime import datetime
import error_logger
import psycopg2
import logging
import time
import json

error_logger.configure_logger("recategorization_error_log.txt")

class MenuItemNotFoundError(Exception):
    """Raised when operation is applied to non-existent menu item"""
    pass


def update_item_category(item_id: str, new_cat: str, cursor_obj: any) -> None:
    try:
        query = """
        UPDATE FROM menu_items
        SET category = %s
        WHERE item_id = %s;
        
        """

        cursor_obj.execute(query, (new_cat, item_id))
        result = cursor_obj.fetchone()
        if not result:
            raise MenuItemNotFoundError

    except psycopg2.Error as db_error:
        print(f"Database failure: {db_error}")
        cursor_obj.rollback()
        msg = f"{item_id}, {new_cat}"
        error_logger.log_error(db_error, msg)

    except MenuItemNotFoundError as menu_error:
        print(f"MenuItemNotFoundError: Tried updating non-existent menu item entry\nDetails: {menu_error}")
        msg = f"{item_id}, {new_cat}"
        error_logger.log_error(menu_error, msg)
    

def update_item_categories(cat_list: list) -> None:
    with dbc.EateryDatabaseConnection as conn:
        cur = conn.cursor()
        for cat_dict in cat_list:
            try:
                item_id = cat_dict["item_id"]
                new_cat = cat_dict["category_new"]
                update_item_category(item_id, new_cat, cur)

            except AttributeError as att:
                msg = f"Incorrect format for '{item_id}, {new_cat}' pair"
                error_logger.log_error(att, msg)



def recategorization():
    try:
        file_path = "recategorized_data.json"
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            cat_list = json.load(file_obj)
            if not isinstance(cat_list, list):
                return
            
        update_item_categories(cat_list)

    except Exception as e:
        pass
