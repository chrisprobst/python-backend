#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# import argparse

from backend.start_webserver import start_webserver

start_webserver(
    "default_config.json",
    "myDatabase.db",
    ""
)
