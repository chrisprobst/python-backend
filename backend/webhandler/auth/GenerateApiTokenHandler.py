#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json
import os

from backend.webhandler.util import BaseHandler
from backend.webhandler.util import PasshashVerifier

class GenerateApiTokenHandler(BaseHandler.BaseHandler):

	def post(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		if self.isInvalidUsername(username):
			self.writeInvalidUsernameResponse()
		elif self.isInvalidPassword(username, password):
			self.writeInvalidPasswordResponse()
		else:
			api_token = self.generateApiToken()
			self.storeApiToken(username, api_token)
			self.writeSuccessResponse(api_token)

	def isInvalidUsername(self, username):
		query = "SELECT * FROM `users` WHERE username=?;"
		userdata = self.context.database.getSingleValueByQuery(query, (username,))
		if userdata == None:
			return True
		return False

	def isInvalidPassword(self, username, password):
		salt_query = "SELECT salt FROM `users` WHERE username=?"
		passhash_query = "SELECT passhash FROM `users` WHERE username=?"
		salt = self.context.database.getSingleValueByQuery(salt_query, (username,))
		passhash = self.context.database.getSingleValueByQuery(passhash_query, (username,))
		return not PasshashVerifier.PasshashVerifier.verify(password, salt, passhash)

	def writeInvalidUsernameResponse(self):
		data = {
			"error": "Invalid username"
		}
		self.write(json.dumps(data))

	def writeInvalidPasswordResponse(self):
		data = {
			"error": "Invalid password"
		}
		self.write(json.dumps(data))

	def writeSuccessResponse(self, api_token):
		data = {
			"access_token": api_token,
			"error": None
		}
		self.write(json.dumps(data))

	def generateApiToken(self):
		return os.urandom(128).encode('hex')

	def storeApiToken(self, username, api_token):
		query = "INSERT INTO api_tokens (username, api_token) VALUES (?,?);"
		args = (username, api_token)
		self.context.database.cursor.execute(query, args)
		self.context.database.commit()







