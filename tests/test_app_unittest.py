import json
import unittest
import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constant_test_cases import VALID_TEST_CASES, INVALID_TEST_CASES,\
    VALIDATION_SCHEMA
import main


TEST_DATABASE_FILE_NAME = "test.db"
TEST_DATA_FILE_NAME = "test_data.json"
TABLES_NAMES = ("goods", "shops_goods")
TABLES_IN_DB_QUERY = "SELECT name FROM sqlite_master WHERE type = 'table'"
DATA = {
    "id": 3,
    "name": "Холодильник",
    "package_params": {
        "width": 120,
        "height": 270
        },
    "location_and_quantity": [
        {
            "location": "Магазин на Ленина",
            "amount": 0
        },
        {
            "location": "Магазин в центре",
            "amount": 9
        }
    ]
}


class TestReadDataFromJsonAndPrepareItForInsertUpdateInDb(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA_FILE_NAME, 'w', encoding='utf-8') as cls.file:
            json.dump(DATA, cls.file)

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_DATA_FILE_NAME)

    def test_reading_data_from_json(self):
        self.assertEqual(main.read_json(TEST_DATA_FILE_NAME), DATA,
                         "read_json function from main.py works incorrect!")

    def test_prepared_data_is_dict(self):
        data_from_json = main.read_json(TEST_DATA_FILE_NAME)
        prepared_data = main.prepare_data_for_insert_update(data_from_json)
        self.assertIsInstance(prepared_data, dict,
                              "prepare_data_for_insert_update function "
                              "should return dictionary!")

    def test_prepared_data_has_needed_keys(self):
        data_from_json = main.read_json(TEST_DATA_FILE_NAME)
        prepared_data = main.prepare_data_for_insert_update(data_from_json)
        prepared_data_keys = set(prepared_data.keys())
        self.assertSetEqual(prepared_data_keys,
                            {"id", "name", "height", "width", "location_and_quantity"},
                            "There is not all needed keys in prepared data")


class TestValidationIncomingData(unittest.TestCase):

    def setUp(self):
        self.validation_schema = VALIDATION_SCHEMA
        self.valid_cases = VALID_TEST_CASES
        self.invalid_cases = INVALID_TEST_CASES

    def test_valid_data(self):
        for valid_case in self.valid_cases:
            self.assertTrue(main.is_data_valid(valid_case, self.validation_schema),
                            "Valid data don't pass a validation!")

    def test_invalid_data(self):
        for valid_case in self.invalid_cases:
            self.assertFalse(main.is_data_valid(valid_case, self.validation_schema),
                            "Invalid data pass a validation!")


class TestCreatingTablesInDatabase(unittest.TestCase):
    conn = None

    @classmethod
    def setUpClass(cls):
        with sqlite3.connect(TEST_DATABASE_FILE_NAME) as cls.conn:
            cls.cur = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        os.remove(TEST_DATABASE_FILE_NAME)

    def test_creation_goods_and_shops_goods_tables_in_database(self):
        main.create_tables_in_db(self.cur)
        self.cur.execute(TABLES_IN_DB_QUERY)
        tables_in_db = set(item[0] for item in self.cur.fetchall())
        for table_name in (TABLES_NAMES):
            self.assertIn(table_name, tables_in_db,
                          f"create_tables_in_db from main.py doesn't create "
                          f"'{table_name}' table in database!")


class TestInsertingUpdatingDataInDatabase(unittest.TestCase):
    conn = None

    @classmethod
    def setUpClass(cls):
        with sqlite3.connect(TEST_DATABASE_FILE_NAME) as cls.conn:
            cls.cur = cls.conn.cursor()
            main.create_tables_in_db(cls.cur)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        os.remove(TEST_DATABASE_FILE_NAME)

    def test_inserting_in_goods_table_works_correct(self):
        data = {
            "id": 100,
            "name": "Микроволновка",
            "height": 30,
            "width": 45,
        }
        main.insert_or_replace_data_to_goods_table(self.cur, data)
        self.cur.execute("SELECT * FROM goods")
        all_data = self.cur.fetchall()
        self.assertIn((data["id"], data["name"], data["height"], data["width"]),
                      all_data, f"{data} haven't inserted in goods table in Database!")

    def test_updating_in_goods_table_works_correct(self):
        data = {
            "id": 1000,
            "name": "ЖК Телевизор",
            "height": 60,
            "width": 130
        }
        main.insert_or_replace_data_to_goods_table(self.cur, data)
        updated_data = {
            "id": 1000,
            "name": "Телевизор",
            "height": 55,
            "width": 120
        }
        main.insert_or_replace_data_to_goods_table(self.cur, updated_data)
        self.cur.execute("SELECT * FROM goods")
        all_data = self.cur.fetchall()
        self.assertNotIn((data["id"], data["name"], data["height"], data["width"]),
                         all_data, f"Outdated data {data} is present after updating in goods table in Database!")
        self.assertIn((updated_data["id"], updated_data["name"], updated_data["height"], updated_data["width"]),
                      all_data, f"Data update haven't happened!")


    def test_inserting_in_shops_goods_table_works_correct(self):
        data = {
            "id": 100,
            "location_and_quantity": [
                {
                    "location": "Магазин на Ленина",
                    "amount": 5
                },
                {
                    "location": "Магазин в центре",
                    "amount": 5
                }
            ]
        }
        main.insert_or_replace_data_to_shops_goods_table(self.cur, data)
        self.cur.execute("SELECT id_good, location, amount FROM shops_goods")
        all_data = self.cur.fetchall()
        for shop in data["location_and_quantity"]:
            self.assertIn((data["id"], shop["location"], shop["amount"]),
                          all_data, f"{data} haven't inserted in shops_goods table in Database!")

    def test_updating_in_shops_goods_table_works_correct(self):
        data = {
            "id": 1000,
            "location_and_quantity": [
                {
                    "location": "Магазин на Ленина",
                    "amount": 3
                },
                {
                    "location": "Магазин в центре",
                    "amount": 3
                }
            ]
        }
        main.insert_or_replace_data_to_shops_goods_table(self.cur, data)
        updated_data = {
            "id": 1000,
            "location_and_quantity": [
                {
                    "location": "Магазин на Ленина",
                    "amount": 0
                },
                {
                    "location": "Магазин в центре",
                    "amount": 0
                }
            ]
        }
        main.insert_or_replace_data_to_shops_goods_table(self.cur, updated_data)
        self.cur.execute("SELECT id_good, location, amount FROM shops_goods")
        all_data = self.cur.fetchall()
        for shop in updated_data["location_and_quantity"]:
            self.assertIn((updated_data["id"], shop["location"], shop["amount"]),
                          all_data, f"{updated_data} haven't inserted in shops_goods table in Database!")
        for shop in data["location_and_quantity"]:
            self.assertNotIn((data["id"], shop["location"], shop["amount"]),
                          all_data, f"Outdated data {data} is present after updating in goods table in Database!")


if __name__ == "__main__":
    unittest.main()
