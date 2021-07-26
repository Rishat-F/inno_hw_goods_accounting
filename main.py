import json
import sqlite3
from sqlite3.dbapi2 import Cursor

import jsonschema
from jsonschema.exceptions import ValidationError


def read_json(json_file: str) -> object:
    """Deserialize JSON-document from JSON-file to a Python object.

    Args:
        json_file: A path to json-file containing JSON document.

    Returns:
        A Python object. For example, it could be dictionary or list.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def is_data_valid(instance, schema) -> bool:
    """Validate an instance under the given schema.

    Args:
        instance: The instance to validate.
        schema: The schema to validate with.

    Returns:
        True if instance valid to schema, False if not.
    """
    try:
        jsonschema.validate(instance, schema)
    except ValidationError as err:
        print("---------------------------")
        print("Данные не прошли валидацию:\n", err, "\n")
        return False
    else:
        return True


def create_tables_in_db(cursor: Cursor) -> None:
    """Create goods and shops_goods tables in database using Cursor object."""
    cursor.executescript("""
                    CREATE TABLE IF NOT EXISTS goods (
                        id INTEGER NOT NULL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        package_height FLOAT NOT NULL,
                        package_width FLOAT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS shops_goods (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        id_good INTEGER NOT NULL,
                        location VARCHAR(100) NOT NULL,
                        amount INTEGER NOT NULL,
                        FOREIGN KEY (id_good) references goods(id)
                    );
                    """
    )


def prepare_data_for_insert_update(data: dict) -> dict:
    """Prepare incoming data for inserting(updating) in database tables."""
    prepared_data = {
        "id": data["id"],
        "name": data["name"],
        "height": data["package_params"]["height"],
        "width": data["package_params"]["width"],
        "location_and_quantity": data["location_and_quantity"]
        }
    return prepared_data


def insert_or_replace_data_to_goods_table(cursor: Cursor,
                                          prepared_data: dict) -> None:
    """Insert goods data or update it if goods already exists in goods table.

    Args:
        cursor: Database Cursor object.
        prepared_data: Incoming data after preparation.
    """
    cursor.execute("""INSERT OR REPLACE INTO goods
                   VALUES (:id, :name, :height, :width)""", prepared_data)


def insert_or_replace_data_to_shops_goods_table(cursor: Cursor,
                                                prepared_data: dict) -> None:
    """Insert goods data or update it if goods already exists
    in shops_goods table.

    Args:
        cursor: Database Cursor object.
        prepared_data: Incoming data after preparation.
    """
    for shop in prepared_data["location_and_quantity"]:
        cursor.execute("""INSERT OR REPLACE INTO shops_goods
                       VALUES (
                           (SELECT id FROM shops_goods
                           WHERE shops_goods.id_good = :id_good and 
                           shops_goods.location = :location),
                           :id_good, :location, :amount)
                       """,
                       {"id_good": prepared_data["id"],
                        "location": shop["location"],
                        "amount": shop["amount"]
                       })


if __name__ == "__main__":
    instance = read_json("data.json")
    schema = read_json("goods.schema.json")
    if is_data_valid(instance, schema):
        prepared_data = prepare_data_for_insert_update(instance)
        with sqlite3.connect("goods.db") as conn:
            cur = conn.cursor()
            create_tables_in_db(cur)
            insert_or_replace_data_to_goods_table(cur, prepared_data)
            insert_or_replace_data_to_shops_goods_table(cur, prepared_data)
