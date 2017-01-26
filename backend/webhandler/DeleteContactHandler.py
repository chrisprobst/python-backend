#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.web
import tornado.escape

from util import ApiHandler
from backend.database.controller import ContactController

"""
Expected input data structure

{
	"contact_id": 1
}

"""

class DeleteContactHandler(ApiHandler.ApiHandler):

	def post(self):
		if self.apiTokenIsInvalid():
			self.writeInvalidApiTokenResponse()
			return
		data = tornado.escape.json_decode(self.get_argument("data"))
		ctr = ContactController.ContactController(self.context.database)
		try:
			ctr.deleteFullJsonContact(data)
			self.writeSuccessResponse()
		except BaseException, e:
			self.writeErrorResponse(e)

	def writeSuccessResponse(self):
		data = {
			"error": None
		}
		self.write(json.dumps(data))