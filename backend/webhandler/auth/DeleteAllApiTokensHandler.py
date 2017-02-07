#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.web

from backend.webhandler.util import ApiHandler

class DeleteAllApiTokensHandler(ApiHandler.ApiHandler):

	def post(self):
		if self.api_token_is_invalid():
			self.write_invalid_api_token_response()
			return
		api_token = self.get_argument("api_token")
		self.deleteAllApiTokens(api_token)
		self.writeSuccessResponse()

	def deleteAllApiTokens(self, api_token):
		username_query = "SELECT username FROM api_tokens WHERE api_token=?;"
		args = (api_token,)
		username = self.context.database.getSingleValueByQuery(username_query, args)
		delete_query = "DELETE FROM api_tokens WHERE username=?;"
		args = (username,)
		self.context.database.cursor.execute(delete_query, args)
		self.context.database.commit()

	def writeSuccessResponse(self):
		data = {
			"error": None
		}
		self.write(json.dumps(data))