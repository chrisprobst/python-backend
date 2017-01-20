#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import tornado.web

class BaseHandler(tornado.web.RequestHandler):

	def initialize(self, context):
		self.context = context