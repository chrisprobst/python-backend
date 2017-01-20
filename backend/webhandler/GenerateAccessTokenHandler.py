#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json
import os

import tornado.web

from util import BaseHandler
from util import PasshashVerifier

class GenerateAccessTokenHandler(BaseHandler.BaseHandler):

	def get(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		if self.isInvalidUsername(username):
			self.writeInvalidUsernameResponse()
		elif self.isInvalidPassword(username, password):
			self.writeInvalidPasswordResponse()
		else:
			access_token = self.generateAccessToken()
			self.storeAccessToken(username, access_token)
			self.writeAccessResponse(access_token)

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
		return not PasshashVerifier.PasshashVerifier().verify(password, salt, passhash)

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

	def writeAccessResponse(self, access_token):
		data = {
			"access_token": access_token,
			"error": None
		}
		self.write(json.dumps(data))

	def generateAccessToken(self):
		return os.urandom(256).encode('hex')

	def storeAccessToken(self, username, access_token):
		query = "INSERT INTO api_tokens (username, api_token) VALUES (?,?);"
		args = (username, access_token)
		self.context.database.cursor.execute(query, args)
		self.context.database.commit()







