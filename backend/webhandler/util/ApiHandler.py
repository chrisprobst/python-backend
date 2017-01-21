#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import BaseHandler

class ApiHandler(BaseHandler.BaseHandler):

	def apiTokenIsInvalid(self):
		api_token = self.get_argument("api_token")
		return self._isInvalidApiToken(api_token)

	def writeInvalidApiTokenResponse(self):
		data = {
			"error": "Invalid API key"
		}
		self.write(json.dumps(data))

	def _isInvalidApiToken(self, api_token):
		query = "SELECT * FROM `api_tokens` WHERE api_token=?;"
		data = self.context.database.getSingleValueByQuery(query, (api_token,))
		if data == None:
			return True
		return False







