#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json


class Config(object):

    def __init__(self, config_path):
        with open(config_path) as settings_file:
            settings_data = json.load(settings_file)
            self.__dict__.update(settings_data)
