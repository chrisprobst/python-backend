#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.web

from util import ApiHandler

class DeleteApiTokenHandler(ApiHandler.ApiHandler):

	def get(self):
		if self.apiTokenIsInvalid():
			self.writeInvalidApiTokenResponse()
			return
		delete_token = self.get_argument("delete_token")
		if self.apiTokenIsNotInDatabase(delete_token):
			self.writeTokenNotFoundResponse()
		else:
			self.deleteApiToken(delete_token)
			self.writeSuccessResponse()

	def apiTokenIsNotInDatabase(self, api_token):
		query = "SELECT * FROM `api_tokens` WHERE api_token=?;"
		data = self.context.database.getSingleValueByQuery(query, (api_token,))
		if data == None:
			return True
		return False

	def deleteApiToken(self, api_token):
		query = "DELETE FROM api_tokens WHERE api_token=?;"
		args = (api_token,)
		self.context.database.cursor.execute(query, args)
		self.context.database.commit()

	def writeTokenNotFoundResponse(self):
		data = {
			"error": "API key to delete not found"
		}
		self.write(json.dumps(data))

	def writeSuccessResponse(self):
		data = {
			"error": None
		}
		self.write(json.dumps(data))

