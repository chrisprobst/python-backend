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
		"id": 1,
		"prefix": "Herr",
		"first_name": "Vorname",
		"last_name": "Nachname",
		"birth_date": "dd.mm.yyy",
		"comment": "Test-Kommentar"
	},
	"mail": [
		{"id": 1, "contact_id": 1, "description": "Test Mail1", "address": "alex1@alex.de"},
		{"id": 2, "contact_id": 1, "description": "Test Mail2", "address": "alex2@alex.de"},
		{"id": 3, "contact_id": 1, "description": "Test Mail3", "address": "alex3@alex.de"}
	],
	"address": [
		{"id": 1, "contact_id": 1, "description": "Privat", "street": "Gilbachstraße", "number": "7-9", "addr_extra": "", "postal": "40219", "city": "Düsseldorf"},
		{"id": 2, "contact_id": 1, "description": "Geschäftlich", "street": "Universitätsstraße", "number": "1", "addr_extra": "", "postal": "40225", "city": "Düsseldorf"}
	],
	"phone": [
		{"id": 1, "contact_id": 1, "description": "Privat1", "number": "0123456789"},
		{"id": 2, "contact_id": 1, "description": "Privat2", "number": "0123456789"},
		{"id": 3, "contact_id": 1, "description": "Privat3", "number": "0123456789"},
		{"id": 4, "contact_id": 1, "description": "Privat4", "number": "0123456789"}
	],
	"study": [
		{"id": 1, "contact_id": 1, "status": "done", "school": "HHU", "course": "Informatik", "start": "dd.mm.yyyy", "end": "dd.mm.yyyy", "focus": "Netzwerksicherheit", "degree": "b_a"},
		{"id": 1, "contact_id": 1, "status": "active",
		 "school": "HHU", "course": "Informatik", "start": "dd.mm.yyyy", "end": "dd.mm.yyyy", "focus": "Nix", "degree": "m_sc"}
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
		contact_id = ctr.insertJsonContact(data["contact"])
		for mail in data["mail"]:
			mail["contact_id"] = contact_id
			ctr.insertJsonMail(mail)
		for address in data["address"]:
			address["contact_id"] = contact_id
			ctr.insertJsonAddress(address)
		for phone in data["phone"]:
			phone["contact_id"] = contact_id
			ctr.insertJsonPhone(phone)
		for study in data["study"]:
			study["contact_id"] = contact_id
			ctr.insertJsonStudy(study)
		self.writeSuccessResponse(contact_id)

	def writeSuccessResponse(self, contact_id):
		data = {
			"contact_id": contact_id,
			"error": None
		}
		self.write(json.dumps(data))