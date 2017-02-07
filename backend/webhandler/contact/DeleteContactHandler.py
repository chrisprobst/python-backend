import json

import tornado.web
import tornado.escape

from backend.webhandler.util import ApiHandler
from backend.database.controller import ContactController


class DeleteContactHandler(ApiHandler.ApiHandler):

    def post(self):
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        data = tornado.escape.json_decode(self.get_argument("data"))
        ctr = ContactController.ContactController(self.context.database)
        try:
            ctr.delete_contact(data)
            self.write_success_response()
        except BaseException, e:
            self.write_error_response(e)
    
    def write_success_response(self):
        data = {
            "error": None
        }
        self.write(json.dumps(data))
