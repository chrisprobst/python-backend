#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.escape

from util import BaseHandler

class ApiHandler(BaseHandler.BaseHandler):

	def get(self):
		data = {
			"error": None
		}
		self.write(json.dumps(data))