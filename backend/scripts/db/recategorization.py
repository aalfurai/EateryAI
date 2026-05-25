import src.db.db_connection as dbc
from datetime import datetime
import scripts.error_logger as error_logger
from pathlib import Path
import psycopg2
import logging
import time
import json

class MenuItemDoestNotExistError(Exception):
    """Raised when operation is applied to non-existent menu item"""
    def __str__(self):
        return "MenuItemDoesNotExistError"

class UpdateFailureError(Exception):
    """An error solely meant to be passed up to function where connection is handled."""
    pass

def update_item_category(item_id: str, new_cat: str, cursor_obj: any) -> None:
    try:
        stripped_item_id = item_id.strip()
        stripped_new_cat = new_cat.strip()

        query = """
        UPDATE menu_items
        SET category = %s
        WHERE item_id = %s;
        
        """

        cursor_obj.execute(query, (stripped_new_cat, stripped_item_id))
        if cursor_obj.rowcount == 0:
            raise MenuItemDoestNotExistError("peepee")
        else:
            # print(f"Successfully recategorized '{item_id}' to: {new_cat}")
            pass


    except MenuItemDoestNotExistError as menu_error:
        print(f"MenuItemNotFoundError: Tried updating non-existent '{item_id}' entry to '{new_cat}'. Details: {menu_error}")
        # print(f"{stripped_item_id}, {stripped_new_cat}")
        msg = f"{item_id}, {new_cat}"
        error_logger.log_error(menu_error, msg)
    

def update_item_categories(cat_list: list) -> None:
    with dbc.EateryDatabaseConnection() as conn:
        cur = conn.cursor()
        for cat_dict in cat_list:
            try:
                item_id = cat_dict["item_id"]
                new_cat = cat_dict["category_new"]
                update_item_category(item_id, new_cat, cur)

            except AttributeError as att:
                msg = f"Incorrect format for '{item_id}, {new_cat}' pair"
                error_logger.log_error(att, msg)

            except psycopg2.Error as db_error:
                print(f"Database failure: {db_error}")
                msg = f"Item={item_id}, New Category={new_cat}"
                error_logger.log_error(db_error, msg)
                conn.rollback()
def recategorization():
    file_path = "data/recategorized/recategorized_data.json"
    with open(file_path, 'r', encoding='utf-8') as file_obj:
        cat_list = json.load(file_obj)
        if not isinstance(cat_list, list):
            return

    update_item_categories(cat_list)

if __name__ == "__main__":
    new_dir = Path("backend") / "data" / "logs"
    new_dir.mkdir(parents=True, exist_ok=True)
    error_logger.configure_logger("recategorization_error_log.txt")
    recategorization()