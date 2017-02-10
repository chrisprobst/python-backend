#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json


class Config(object):

    def __init__(self, config_path, logger):
        with open(config_path) as settings_file:
            logger.info("Load configuration file: {path}".format(path=config_path))
            settings_data = json.load(settings_file)
            for key, value in settings_data.iteritems():
                output = "config: {key}={value}"
                logger.debug(output.format(key=key, value=value))
            self.__dict__.update(settings_data)
