import json
import sqlite3

import jsonschema
from jsonschema.exceptions import ValidationError


def read_json(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def is_json_valid(instance, schema) -> bool:
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
        print("Данные не прошли валидацию", err)
        return False
    else:
        return True


def create_tables_in_db_if_not_exists(cursor):
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS goods (
                        id INTEGER NOT NULL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        package_height FLOAT NOT NULL,
                        package_width FLOAT NOT NULL
                    );
                    """
    )
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS shops_goods (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        id_good INTEGER NOT NULL,
                        location VARCHAR(100) NOT NULL,
                        amount INTEGER NOT NULL,
                        FOREIGN KEY (id_good) references goods(id)
                    );
                    """
    )


def get_all_data_from_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name};")
    all_data = cursor.fetchall()
    return all_data


def get_all_id_from_goods_table(cursor):
    cursor.execute(f"SELECT id FROM goods;")
    all_data = cursor.fetchall()
    return all_data


def prepare_data_for_insert_update(data):
    prepared_data = {
        "id": data["id"],
        "name": data["name"],
        "height": data["package_params"]["height"],
        "width": data["package_params"]["width"],
        "location_and_quantity": data["location_and_quantity"]
        }
    return prepared_data


def insert_or_replace_data_to_goods_table(cursor, data):
    cursor.execute("""INSERT OR REPLACE INTO goods
                   VALUES (:id, :name, :height, :width)""", data)


def insert_or_replace_data_to_shops_goods_table(cursor, data):
    cursor.execute("""INSERT OR REPLACE INTO shops_goods
                   VALUES (
                       (SELECT id FROM shops_goods
                       WHERE shops_goods.id_good = :id and shops_goods.location = :location),
                       :id, :location, :amount)
                   """, data)


if __name__ == "__main__":
    instance = read_json("data.json")
    schema = read_json("goods.schema.json")
    if is_json_valid(instance, schema):
        with sqlite3.connect("goods.db") as con:
            cur = con.cursor()
            create_tables_in_db_if_not_exists(cur)
            prepared_data = prepare_data_for_insert_update(instance)
            insert_or_replace_data_to_goods_table(cur, prepared_data)
            for shop in prepared_data["location_and_quantity"]:
                insert_or_replace_data_to_shops_goods_table(cur,
                    {"id": prepared_data["id"],
                     "location": shop["location"],
                     "amount": shop["amount"]
                     })
