#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json
import os

from backend.webhandler.util import BaseHandler
from backend.webhandler.util import PasshashVerifier


class GenerateApiTokenHandler(BaseHandler.BaseHandler):
    
    @staticmethod
    def generate_api_token():
        """
        Generates a 128 bit nonce as a string that only contains hex digits based on os.random
        :return: (str) The generated nonce
        """
        return os.urandom(128).encode('hex')
    
    def post(self):
        """
        Post handler of GenerateApiTokenHandler
        :return: (none)
        """
        username = self.get_argument("username")
        password = self.get_argument("password")
        if self.is_invalid_username(username):
            self.write_invalid_username_response()
        elif self.is_invalid_password(username, password):
            self.write_invalid_password_response()
        else:
            api_token = self.generate_api_token()
            self.store_api_token(username, api_token)
            self.write_success_response(api_token)
    
    def is_invalid_username(self, username):
        """
        Returns True if given string is not a valid username
        :param username: (str) The username to test
        :return: (bool)
        """
        query = "SELECT * FROM `users` WHERE username=?;"
        userdata = self.context.database.get_single_value_by_query(query, (username,))
        if userdata is not None:
            return True
        return False
    
    def is_invalid_password(self, username, password):
        """
        Returns True if the given pair of username and password is not valid
        :param username: (str) The username to verify
        :param password: (str) The password to verify
        :return: (bool)
        """
        salt_query = "SELECT salt FROM `users` WHERE username=?"
        passhash_query = "SELECT passhash FROM `users` WHERE username=?"
        salt = self.context.database.get_single_value_by_query(salt_query, (username,))
        passhash = self.context.database.get_single_value_by_query(passhash_query, (username,))
        return not PasshashVerifier.PasshashVerifier.verify(password, salt, passhash)
    
    def write_invalid_username_response(self):
        """
        Writes a JSON answer with an error message (invalid username)
        :return: (none)
        """
        data = {
            "error": "Invalid username"
        }
        self.write(json.dumps(data))
    
    def write_invalid_password_response(self):
        """
        Writes a JSON answer with an error message (invalid password)
        :return: (none)
        """
        data = {
            "error": "Invalid password"
        }
        self.write(json.dumps(data))
    
    def write_success_response(self, api_token):
        """
        Write a JSON answer containing the generated API token for a successfull login request
        :param api_token: (str) The generated API token
        :return: (none)
        """
        data = {
            "access_token": api_token,
            "error": None
        }
        self.write(json.dumps(data))
    
    def store_api_token(self, username, api_token):
        """
        Stores a generated API token in the database and relates it to one database user
        :param username: (str) The username
        :param api_token: (str) The API token
        :return: (none)
        """
        query = "INSERT INTO api_tokens (username, api_token) VALUES (?,?);"
        args = (username, api_token)
        self.context.database.cursor.execute(query, args)
        self.context.database.commit()
