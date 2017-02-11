# coding=utf-8

from __future__ import absolute_import

import logging
import unittest

from backend.database import Database


class DatabaseTest(unittest.TestCase):
    """
    This test contains the entire database structure how it should be set up.
    Whenever a database change is required, apply them to this test. The dict
    TABLES maps every existing table name to its columns and types. For the
    project this TestCase is the definition of our model (i.e. the database).
    """
    
    TABLES = {
        "contact": {
            "primary": [
                ("id", "INT")
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
                ("id", "INT")
            ],
            "not_primary": [
                ("contact_id", "INT"),
                ("description", "TEXT"),
                ("address", "TEXT")
            ]
        },
        "phone": {
            "primary": [
                ("id", "INT")
            ],
            "not_primary": [
                ("contact_id", "INT"),
                ("description", "TEXT"),
                ("number", "TEXT")
            ]
        },
        "address": {
            "primary": [
                ("id", "INT")
            ],
            "not_primary": [
                ("contact_id", "INT"),
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
                ("id", "INT")
            ],
            "not_primary": [
                ("contact_id", "INT"),
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
                ("contact_id", "INT")
            ],
            "not_primary": [
                ("ressort", "TEXT"),
                ("active", "TEXT"),
                ("position", "TEXT"),
                ("joined", "DATE"),
                ("left", "DATE")
            ]
        },
        "users": {
            "primary": [
                ("username", "INT")
            ],
            "not_primary": [
                ("passhash", "TEXT"),
                ("salt", "TEXT"),
                ("date", "DATE")
            ]
        },
        "api_tokens": {
            "primary": [
                ("username", "TEXT"),
                ("api_token", "TEXT")
            ]
        }
    }
    
    QUERY_GET_TABLE_NAME = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
    QUERY_GET_ALL_TABLE_NAMES = "SELECT name FROM sqlite_master WHERE type='table';"
    
    MESSAGE_TABLE_NOT_FOUND = "Table '{table_name}' not found."
    MESSAGE_INVALID_TABLE = "Tables '{invalid_tables}' should not exist."
    
    def setUp(self):
        self.database = Database.Database(":memory:", logging.getLogger("test"))
    
    def test_tables_exist(self):
        table_names = DatabaseTest.TABLES.keys()
        for table_name in table_names:
            self.database.cursor.execute(DatabaseTest.QUERY_GET_TABLE_NAME, (table_name,))
            result = self.database.cursor.fetchall()
            self.assertTrue(
                result,
                DatabaseTest.MESSAGE_TABLE_NOT_FOUND.format(
                    table_name=table_name
                )
            )
    
    def test_unwanted_tables(self):
        table_names = set(DatabaseTest.TABLES.keys())
        self.database.cursor.execute(DatabaseTest.QUERY_GET_ALL_TABLE_NAMES)
        results = [r[0] for r in self.database.cursor.fetchall()]
        filtered_results = filter(lambda r: not r.startswith("sqlite_"), results)
        existing_tables = set(filtered_results)
        invalid_tables = existing_tables.difference(table_names)
        self.assertFalse(
            invalid_tables,
            DatabaseTest.MESSAGE_INVALID_TABLE.format(
                invalid_tables=invalid_tables
            )
        )

suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTest)
unittest.TextTestRunner(verbosity=2).run(suite)