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
        username = tornado.escape(self.get_argument("username"))
        password = tornado.escape(self.get_argument("password"))
        ctr = AuthController.AuthController(self.context.database)
        try:
            api_token = ctr.check_token(username, password)
            self.write_success_response(api_token)
        except BaseException, e:
            exception_text = str(e)
            if(exception_text == "InvalidUser"):
                self.write_invalid_username_response()
            elif(exception_text == "InvalidPassword"):
                self.write_invalid_password_response()
            else:
                self.write_error_response(e)

    def write_error_response(self, e):
        """
        Writes a JSON answer with an error message
        :param e: The given error to print
        :return: (none)
        """
        data = {
            "error": repr(e)
        }
        self.write(json.dumps(data))

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