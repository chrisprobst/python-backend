#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json
import tornado.escape

from backend.webhandler.util import ApiHandler
from backend.database.controller import ContactController


class SelectContactsBySearchHandler(ApiHandler.ApiHandler):
    
    def post(self):
        """
        Post handler for SelectAllContactsHandler
        :return: (none)
        """
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        data = tornado.escape.json_decode(self.get_argument("data"))
        ctr = ContactController.ContactController(self.context.database)
        try:
            result = ctr.select_contacts_by_search(data)
            self.write_success_response(result)
        except BaseException, e:
            self.write_error_response(e)
    
    def write_success_response(self, result):
        """
        Write a success JSON response containing all available contacts
        :param result: (dict) Contact structures
        :return: (none)
        """
        data = {
            "result": result,
            "error": None
        }
        self.write(json.dumps(data))
