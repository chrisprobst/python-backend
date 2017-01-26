#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import json

import tornado.web
import tornado.escape

from util import ApiHandler
from backend.database.controller import ContactController

"""
Expected input data structure

{
	"contact": {
		"prefix": "Herr",
		"first_name": "Vorname",
		"last_name": "Nachname",
		"birth_date": "dd.mm.yyy",
		"comment": "Test-Kommentar"
	},
	"mail": [
		{"description": "Test Mail1", "address": "alex1@alex.de"},
		{"description": "Test Mail2", "address": "alex2@alex.de"},
		{"description": "Test Mail3", "address": "alex3@alex.de"}
	],
	"address": [
		{"description": "Privat", "street": "Gilbachstraße", "number": "7-9", "addr_extra": "", "postal": "40219", "city": "Düsseldorf"},
		{"description": "Geschäftlich", "street": "Universitätsstraße", "number": "1", "addr_extra": "", "postal": "40225", "city": "Düsseldorf"}
	],
	"phone": [
		{"description": "Privat1", "number": "0123456789"},
		{"description": "Privat2", "number": "0123456789"},
		{"description": "Privat3", "number": "0123456789"},
		{"description": "Privat4", "number": "0123456789"}
	],
	"study": [
		{"status": "done", "school": "HHU", "course": "Informatik", "start": "dd.mm.yyyy", "end": "dd.mm.yyyy", "focus": "Netzwerksicherheit", "degree": "b_a"},
		{"status": "active", "school": "HHU", "course": "Informatik", "start": "dd.mm.yyyy", "end": "dd.mm.yyyy", "focus": "Nix", "degree": "m_sc"}
	]
}

"""

class CreateContactHandler(ApiHandler.ApiHandler):

	def post(self):
		if self.apiTokenIsInvalid():
			self.writeInvalidApiTokenResponse()
			return
		data = tornado.escape.json_decode(self.get_argument("data"))
		ctr = ContactController.ContactController(self.context.database)
		try:
			contact_id = ctr.insertFullJsonContact(data)
			self.writeSuccessResponse(contact_id)
		except BaseException, e:
			self.writeErrorRespone(e)

	def writeSuccessResponse(self, contact_id):
		data = {
			"contact_id": contact_id,
			"error": None
		}
		self.write(json.dumps(data))