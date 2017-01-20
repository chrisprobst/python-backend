#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

class WebhandlerContext(object):

	def __init__(self, config, database, renderer, logger):
		self.config = config
		self.database = database
		self.renderer = renderer
		self.logger = logger