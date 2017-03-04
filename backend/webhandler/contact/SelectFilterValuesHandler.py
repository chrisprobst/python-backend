#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

from backend.webhandler.util import ApiHandler
from backend.database.controller import ContactController


class SelectFilterValuesHandler(ApiHandler.ApiHandler):

    def post(self):
        """
        Post handler for SelectFilterValuesHandler
        :return: (none)
        """
        ctr = ContactController.ContactController(self.context.database)
        self.api_post(ctr.select_filter_values)
