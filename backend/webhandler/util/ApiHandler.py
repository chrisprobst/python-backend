import json

import BaseHandler


class ApiHandler(BaseHandler.BaseHandler):

    def api_token_is_invalid(self):
        api_token = self.get_argument("api_token")
        return self._is_invalid_api_token(api_token)
    
    def write_invalid_api_token_response(self):
        data = {
            "error": "Invalid API key"
        }
        self.write(json.dumps(data))
    
    def write_error_response(self, e):
        data = {
            "error": repr(e)
        }
        self.write(json.dumps(data))
    
    def _is_invalid_api_token(self, api_token):
        query = "SELECT * FROM `api_tokens` WHERE api_token=?;"
        data = self.context.database.getSingleValueByQuery(query, (api_token,))
        if not data:
            return True
        return False
