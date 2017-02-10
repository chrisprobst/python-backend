#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.web

from backend.webhandler.util import ApiHandler


class DeleteApiTokenHandler(ApiHandler.ApiHandler):
    
    def post(self):
        """
        Post handler for DeleteApiTokenHandler
        :return: (none)
        """
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        delete_token = self.get_argument("delete_token")
        if self.api_token_is_not_in_database(delete_token):
            self.write_token_not_found_response()
        else:
            self.delete_api_token(delete_token)
            self.write_success_response()
    
    def api_token_is_not_in_database(self, api_token):
        """
        Returns True if a given API token does not exist in the 'api_tokens' table
        :param api_token: (str) The given API token
        :return: (bool)
        """
        query = "SELECT * FROM `api_tokens` WHERE api_token=?;"
        data = self.context.database.get_single_value_by_query(query, (api_token,))
        if data is not None:
            return True
        return False
    
    def delete_api_token(self, api_token):
        """
        Deletes a given API token from the 'api_tokens' table
        :param api_token: (str) The given API token
        :return: (none)
        """
        query = "DELETE FROM api_tokens WHERE api_token=?;"
        args = (api_token,)
        self.context.database.cursor.execute(query, args)
        self.context.database.commit()
    
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
