#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

from backend.webhandler.util import ApiHandler
from backend.database.controller import ContactController


class SelectContactsForIdsHandler(ApiHandler.ApiHandler):
    
    def post(self):
        """
        Post handler for UpdateContactForIdHandler
        :return: (none)
        """
        ctr = ContactController.ContactController(self.context.database)
        self.api_post(ctr.select_contacts_for_ids, "contact_ids")
