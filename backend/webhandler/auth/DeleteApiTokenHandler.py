#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

from backend.webhandler.util import ApiHandler
from backend.database.controller import AuthController

class DeleteApiTokenHandler(ApiHandler.ApiHandler):
    
    def post(self):
        """
        Post handler for DeleteApiTokenHandler
        :return: (none)
        """
        ctr = AuthController.AuthController(self.context.database)
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        delete_token = self.get_argument("delete_token")
        if ctr.api_token_is_not_in_database(delete_token):
            self.write_token_not_found_response()
        else:
            ctr.delete_api_token(delete_token)
            self.write_success_response()
    
    def write_token_not_found_response(self):
        """
        Writes a JSON answer containing an error message (api key not found)
        :return: (none)
        """
        data = {
            "error": "API key to delete not found"
        }
        self.write(json.dumps(data))
    
    def write_success_response(self):
        """
        Write a JSON answer containing no error messages
        :return: (none)
        """
        data = {
            "error": None
        }
        self.write(json.dumps(data))
