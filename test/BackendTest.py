# coding=utf-8

from unittest import TestLoader, TextTestRunner

from test.config.ConfigTest import ConfigTest
from test.database.DatabaseTest import DatabaseTest
from test.database.controller.BaseControllerTest import BaseControllerTest

test_loader = TestLoader()
test_runner = TextTestRunner(verbosity=2)

config_suite = test_loader.loadTestsFromTestCase(ConfigTest)
database_suite = test_loader.loadTestsFromTestCase(DatabaseTest)
basecontroller_suite = test_loader.loadTestsFromTestCase(BaseControllerTest)

test_runner.run(config_suite)
test_runner.run(database_suite)
test_runner.run(basecontroller_suite)

# TODO: add more tests here!