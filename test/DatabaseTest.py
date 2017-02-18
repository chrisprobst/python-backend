# coding=utf-8

from __future__ import absolute_import

import logging
import unittest

from backend.database import Database


class DatabaseTest(unittest.TestCase):
    """
    This test contains the entire database structure how it should be set up.
    Whenever database changes are required, apply them to this test. The dict
    TABLES maps every existing table name to its columns and types. For the
    project this TestCase is the definition of our model (i.e. the database).
    """
    
    TABLES = {
        "contact": {
            "primary": [
                ("id", "INTEGER")
            ],
            "not_primary": [
                ("prefix", "TEXT"),
                ("first_name", "TEXT"),
                ("last_name", "TEXT"),
                ("birth_date", "DATE"),
                ("comment", "TEXT")
            ]
        },
        "mail": {
            "primary": [
                ("id", "INTEGER")
            ],
            "not_primary": [
                ("contact_id", "INTEGER"),
                ("description", "TEXT"),
                ("address", "TEXT")
            ]
        },
        "phone": {
            "primary": [
                ("id", "INTEGER")
            ],
            "not_primary": [
                ("contact_id", "INTEGER"),
                ("description", "TEXT"),
                ("number", "TEXT")
            ]
        },
        "address": {
            "primary": [
                ("id", "INTEGER")
            ],
            "not_primary": [
                ("contact_id", "INTEGER"),
                ("description", "TEXT"),
                ("street", "TEXT"),
                ("number", "TEXT"),
                ("addr_extra", "TEXT"),
                ("postal", "TEXT"),
                ("city", "TEXT")
            ]
        },
        "study": {
            "primary": [
                ("id", "INTEGER")
            ],
            "not_primary": [
                ("contact_id", "INTEGER"),
                ("status", "TEXT"),
                ("school", "TEXT"),
                ("course", "TEXT"),
                ("start", "DATE"),
                ("end", "DATE"),
                ("focus", "TEXT"),
                ("degree", "TEXT")
            ]
        },
        "member": {
            "primary": [
                ("contact_id", "INTEGER")
            ],
            "not_primary": [
                ("ressort", "TEXT"),
                ("active", "INTEGER"),
                ("position", "TEXT"),
                ("joined", "DATE"),
                ("left", "DATE")
            ]
        },
        "users": {
            "primary": [
                ("username", "TEXT")
            ],
            "not_primary": [
                ("passhash", "TEXT"),
                ("salt", "TEXT"),
                ("created", "DATE")
            ]
        },
        "api_tokens": {
            "primary": [
                ("username", "TEXT"),
                ("api_token", "TEXT")
            ],
            "not_primary": []
        }
    }
    
    QUERY_GET_TABLE_NAME = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
    QUERY_GET_ALL_TABLE_NAMES = "SELECT name FROM sqlite_master WHERE type='table';"
    QUERY_GET_TABLE_INFO = "PRAGMA table_info({});"
    
    MESSAGE_TABLE_NOT_FOUND = "Table '{table_name}' not found."
    MESSAGE_INVALID_TABLE = "Tables '{invalid_tables}' should not exist."
    MESSAGE_UNEQUAL_COLUMN_TYPES = "Column {table}.{column} was expected to be '{expected}' " +\
        "but was '{found}'"
    
    def setUp(self):
        self.database = Database.Database(":memory:", logging.getLogger("test"))
        self.table_names = DatabaseTest.TABLES.keys()
    
    def test_tables_exist(self):
        for table_name in self.table_names:
            self.database.cursor.execute(DatabaseTest.QUERY_GET_TABLE_NAME, (table_name,))
            result = self.database.cursor.fetchall()
            self.assertTrue(
                result,
                DatabaseTest.MESSAGE_TABLE_NOT_FOUND.format(
                    table_name=table_name
                )
            )
    
    def test_unwanted_tables(self):
        self.database.cursor.execute(DatabaseTest.QUERY_GET_ALL_TABLE_NAMES)
        results = [r[0] for r in self.database.cursor.fetchall()]
        filtered_results = filter(lambda r: not r.startswith("sqlite_"), results)
        existing_tables = set(filtered_results)
        invalid_tables = existing_tables.difference(self.table_names)
        self.assertFalse(
            invalid_tables,
            DatabaseTest.MESSAGE_INVALID_TABLE.format(
                invalid_tables=invalid_tables
            )
        )
    
    def test_columns_exist(self):
        pass
    
    def test_column_types(self):
        for table_name in self.table_names:
            self.database.cursor.execute(DatabaseTest.QUERY_GET_TABLE_INFO.format(table_name))
            result = self.database.cursor.fetchall()
            columns = self._get_all_columns_for_table(table_name)
            column_name_to_type = dict([(e[1], e[2]) for e in result])
            for column, expected_type in columns:
                found_type = column_name_to_type[column]
                self.assertEqual(
                    expected_type,
                    found_type,
                    DatabaseTest.MESSAGE_UNEQUAL_COLUMN_TYPES.format(
                        table=table_name,
                        column=column,
                        expected=expected_type,
                        found=found_type
                    )
                )
    
    def _get_all_columns_for_table(self, table_name):
        return DatabaseTest.TABLES[table_name]["primary"] + DatabaseTest.TABLES[table_name]["not_primary"]
        

suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTest)
unittest.TextTestRunner(verbosity=2).run(suite)