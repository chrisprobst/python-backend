#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.escape
import tornado.web

class ApiHandler(tornado.web.RequestHandler):

	def initialize(self, context):
		self.context = context

	def get(self):
		data = {
			"error": None
		}
		self.write(json.dumps(data))