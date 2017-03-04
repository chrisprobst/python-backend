#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

from backend.webhandler.util import ApiHandler
from backend.database.controller import ContactController


class CreateContactHandler(ApiHandler.ApiHandler):

    def post(self):
        """
        Post handler for CreateContactHandler
        :return: (none)
        """
        ctr = ContactController.ContactController(self.context.database)
        self.api_post(ctr.create_contact)
