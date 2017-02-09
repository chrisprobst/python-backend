#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.escape

from backend.webhandler.util import ApiHandler
from backend.database.controller import ContactController

import traceback

class SelectContactForIdHandler(ApiHandler.ApiHandler):

    def post(self):
        """
        Post handler for SelectContactForIdHandler
        :return: (none)
        """
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        data = tornado.escape.json_decode(self.get_argument("data"))
        # TODO: At least wrap ith try/except!
        contact_id = data["contact_id"]
        ctr = ContactController.ContactController(self.context.database)
        try:
            result = ctr.select_contact_for_id(contact_id)
            self.write_success_response(result)
        except BaseException, e:
            print traceback.format_exc()
            self.write_error_response(e)
    
    def write_success_response(self, result):
        """
        TODO: remove this method to parent class
        """
        data = {
            "result": result,
            "error": None
        }
        self.write(json.dumps(data))