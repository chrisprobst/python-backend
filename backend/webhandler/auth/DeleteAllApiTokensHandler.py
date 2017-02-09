#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

from backend.webhandler.util import ApiHandler


class DeleteAllApiTokensHandler(ApiHandler.ApiHandler):

    def post(self):
        """
        Post handler for DeleteAllApiTokensHandler
        :return: (none)
        """
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        api_token = self.get_argument("api_token")
        self.delete_all_api_tokens(api_token)
        self.write_success_response()
    
    def delete_all_api_tokens(self, api_token):
        """
        Determines the user id for a given token and deletes all API tokens for that id
        :param api_token: (str) A valid API token
        :return: (none)
        """
        username_query = "SELECT username FROM api_tokens WHERE api_token=?;"
        args = (api_token,)
        username = self.context.database.getSingleValueByQuery(username_query, args)
        delete_query = "DELETE FROM api_tokens WHERE username=?;"
        args = (username,)
        self.context.database.cursor.execute(delete_query, args)
        self.context.database.commit()
    
    def write_success_response(self):
        """
        Write a JSON answer containing no error messages
        :return: (none)
        """
        data = {
            "error": None
        }
        self.write(json.dumps(data))
