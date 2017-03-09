#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

from backend.webhandler.util import ApiHandler
from backend.database.controller import AuthController

class DeleteAllApiTokensHandler(ApiHandler.ApiHandler):

    def post(self):
        """
        Post handler for DeleteAllApiTokensHandler
        :return: (none)
        """
        ctr = AuthController.AuthController(self.context.database)
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        api_token = self.get_argument("api_token")
        ctr.delete_all_api_tokens(api_token)
        self.write_success_response()

    def write_success_response(self):
        """
        Write a JSON answer containing no error messages
        :return: (none)
        """
        data = {
            "error": None
        }
        self.write(json.dumps(data))
