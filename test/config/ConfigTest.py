# coding=utf-8

from __future__ import absolute_import

import logging
import tempfile
import unittest

from backend.config import Config

TEST_CONFIG = """
{
    "number": 1,
    "store": {
        "value_1": "test string",
        "value_2": null
    }
}
"""


class ConfigTest(unittest.TestCase):
    
    WRONG_TYPE_MESSAGE = "Wrong type: {type}"
    WRONG_VALUE_MESSAGE = "Wrong value: {value}"
    
    def setUp(self):
        self.config_file = tempfile.NamedTemporaryFile("w")
        self.config_file.write(TEST_CONFIG)
        self.config_file.seek(0)
        self.config = Config.Config(self.config_file.name, logging.getLogger("test"))
    
    def tearDown(self):
        self.config_file.close()
    
    def test_types(self):
        self.assertIsInstance(
            self.config.number,
            int,
            ConfigTest.WRONG_TYPE_MESSAGE.format(
                type=str(type(self.config.number))
            )
        )
        self.assertIsInstance(
            self.config.store,
            dict,
            ConfigTest.WRONG_TYPE_MESSAGE.format(
                type=str(type(self.config.store))
            )
        )
        self.assertIsInstance(
            self.config.store["value_1"],
            unicode,
            ConfigTest.WRONG_TYPE_MESSAGE.format(
                type=str(type(self.config.store["value_1"]))
            )
        )
        self.assertIsInstance(
            self.config.store["value_2"],
            type(None),
            ConfigTest.WRONG_TYPE_MESSAGE.format(
                type=str(type(self.config.store["value_2"]))
            )
        )
    
    def test_access(self):
        self.assertEqual(
            self.config.number,
            1,
            ConfigTest.WRONG_VALUE_MESSAGE.format(
                value=self.config.number
            )
        )
        self.assertEqual(
            self.config.store["value_1"],
            "test string",
            ConfigTest.WRONG_VALUE_MESSAGE.format(
                value=self.config.store["value_1"]
            )
        )
        self.assertEqual(
            self.config.store["value_2"],
            None,
            ConfigTest.WRONG_VALUE_MESSAGE.format(
                value=self.config.store["value_2"]
            )
        )

suite = unittest.TestLoader().loadTestsFromTestCase(ConfigTest)
unittest.TextTestRunner(verbosity=2).run(suite)
