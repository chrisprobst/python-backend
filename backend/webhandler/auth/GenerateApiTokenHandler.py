#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json
import tornado.escape
from backend.webhandler.util import BaseHandler
from backend.database.controller import AuthController


class GenerateApiTokenHandler(BaseHandler.BaseHandler):
    
    def post(self):
        """
        Post handler of GenerateApiTokenHandler
        :return: (none)
        """
        username = self.get_argument("username")
        password = self.get_argument("password")
        ctr = AuthController.AuthController(self.context.database)
        try:
            api_token = ctr.check_token(username, password)
            self.write_success_response(api_token)
        except BaseException, e:
            self.write_error_response(str(e))

    def write_error_response(self, e):
        """
        Writes a JSON answer with an error message
        :param e: The given error to print
        :return: (none)
        """
        data = {
            "error": e
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