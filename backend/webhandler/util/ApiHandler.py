#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json
import tornado.escape
import traceback

import BaseHandler


class ApiHandler(BaseHandler.BaseHandler):
    
    def api_post(self, callback, data_key=''):
        """
        general api post handler for all handler
        :return: (none)
        """
        if self.api_token_is_invalid():
            self.write_invalid_api_token_response()
            return
        try:
            data = tornado.escape.json_decode(self.get_argument("data"))
        except BaseException:
            data = ''
        try:
            if data_key:
                data = data[data_key]
            if data:
                result = callback(data)
            else:
                result = callback()
            self.write_success_response(result)
        except BaseException, e:
            print traceback.format_exc()
            self.write_error_response(e)
    
    def write_success_response(self, result):
        """
        Write a success JSON response
        :param result
        :return: (none)
        """
        data = {
            "result": result,
            "error": None
        }
        self.write(json.dumps(data))
    
    LOG_INVALID_API_TOKEN = "Received invalid api token {token}"

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
        data = self.context.database.get_single_value_by_query(query, (api_token,))
        if not data:
            self.context.logger.debug(ApiHandler.LOG_INVALID_API_TOKEN.format(token=api_token))
            return True
        return False
