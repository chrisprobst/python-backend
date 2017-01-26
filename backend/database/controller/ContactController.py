class ContactController(object):

	# Set fields that will be inserted into table (note: this is important because
	# there might exist fields like the ID that are not inserted manually)
	INSERT_COLUMNS = {
		"contact": ("prefix", "first_name", "last_name", "birth_date", "comment"),
		"mail": ("contact_id", "description", "address"),
		"phone": ("contact_id", "description", "number"),
		"address": ("contact_id", "description", "street", "number", "addr_extra", "postal", "city"),
		"study": ("contact_id", "status", "school", "course", "start", "end", "focus", "degree")
	}

	INSERT_QUERIES = {
		"contact": "INSERT INTO `contact` (prefix, first_name, last_name, birth_date, comment) VALUES (?,?,?,?,?);",
		"mail": "INSERT INTO `mail` (contact_id, description, address) VALUES (?,?,?);",
		"phone": "INSERT INTO `phone` (contact_id, description, number) VALUES (?,?,?);",
		"address": "INSERT INTO `address` (contact_id, description, street, number, addr_extra, postal, city) VALUES (?,?,?,?,?,?,?);",
		"study": "INSERT INTO `study` (contact_id, status, school, course, start, end, focus, degree) VALUES (?,?,?,?,?,?,?,?);"
	}

	UPDATE_COLUMNS = {
		"contact": ("prefix", "first_name", "last_name", "birth_date", "comment", "id"),
		"mail": ("description", "address", "contact_id"),
		"phone": ("description", "number", "contact_id"),
		"address": ("description", "street", "number", "addr_extra", "postal", "city", "contact_id"),
		"study": ("status", "school", "course", "start", "end", "focus", "degree", "contact_id")
	}

	UPDATE_QUERIES = {
		"contact": "UPDATE contact SET prefix=?,first_name=?,last_name=?,birth_date=?,comment=? WHERE id=?;",
		"mail": "UPDATE `mail` SET description=?,address=? WHERE contact_id=?;",
		"phone": "UPDATE `phone` SET description=?,number=? WHERE contact_id=?;",
		"address": "UPDATE `address` SET description=?,street=?,number=?,addr_extra=?,postal=?,city=? WHERE contact_id=?;",
		"study": "UPDATE `study` SET status=?,school=?,course=?,start=?,end=?,focus=?,degree=? WHERE contact_id=?;"
	}

	DELETE_COLUMNS = {
		"contact": ("id",),
		"mail": ("contact_id",),
		"phone": ("contact_id",),
		"address": ("contact_id",),
		"study": ("contact_id",),
	}

	DELETE_QUERIES = {
		"contact": "DELETE FROM `contact` WHERE id=?;",
		"mail": "DELETE FROM `mail` WHERE contact_id=?;",
		"phone": "DELETE FROM `phone` WHERE contact_id=?;",
		"address": "DELETE FROM `address` WHERE contact_id=?;",
		"study": "DELETE FROM `study` WHERE contact_id=?;"
	}

	def __init__(self, database):
		self.database = database

	def insertFullJsonContact(self, json):
		try:
			contact_id = self._insertJsonInTable(json["contact"], "contact")
			for mail in json["mail"]:
				mail["contact_id"] = contact_id
				self._insertJsonInTable(mail, "mail")
			for address in json["address"]:
				address["contact_id"] = contact_id
				self._insertJsonInTable(address, "address")
			for phone in json["phone"]:
				phone["contact_id"] = contact_id
				self._insertJsonInTable(phone, "phone")
			for study in json["study"]:
				study["contact_id"] = contact_id
				self._insertJsonInTable(study, "study")
			self.database.commit()
			return contact_id
		except BaseException, e:
			self.database.rollback()
			raise e

	def updateFullJsonContact(self, json):
		try:
			self._updateJsonInTable(json["contact"], "contact")
			for mail in json["mail"]:
				self._updateJsonInTable(mail, "mail")
			for address in json["address"]:
				self._updateJsonInTable(address, "address")
			for phone in json["phone"]:
				self._updateJsonInTable(phone, "phone")
			for study in json["study"]:
				self._updateJsonInTable(study, "study")
			self.database.commit()
		except BaseException, e:
			self.database.rollback()
			raise e

	def deleteFullJsonContact(self, json):
		try:
			self._deleteJsonInTable(json["contact"], "contact")
			for mail in json["mail"]:
				self._deleteJsonInTable(mail, "mail")
			for address in json["address"]:
				self._deleteJsonInTable(address, "address")
			for phone in json["phone"]:
				self._deleteJsonInTable(phone, "phone")
			for study in json["study"]:
				self._deleteJsonInTable(study, "study")
			self.database.commit()
		except BaseException, e:
			self.database.rollback()
			raise e

	def insertJsonContact(self, json):
		return self._insertJsonInTable(json, "contact", commit=True)

	def insertJsonMail(self, json):
		return self._insertJsonInTable(json, "mail", commit=True)

	def insertJsonPhone(self, json):
		return self._insertJsonInTable(json, "phone", commit=True)

	def insertJsonAddress(self, json):
		return self._insertJsonInTable(json, "address", commit=True)

	def insertJsonStudy(self, json):
		return self._insertJsonInTable(json, "study", commit=True)

	def updateJsonContact(self, json):
		self._updateJsonInTable(json, "contact", commit=True)

	def updateJsonMail(self, json):
		self._updateJsonInTable(json, "mail", commit=True)

	def updateJsonPhone(self, json):
		self._updateJsonInTable(json, "phone", commit=True)

	def updateJsonAddress(self, json):
		self._updateJsonInTable(json, "address", commit=True)

	def updateJsonStudy(self, json):
		self._updateJsonInTable(json, "study", commit=True)

	def deleteJsonContact(self, json):
		self._deleteJsonInTable(json, "contact", commit=True)

	def deleteJsonMail(self, json):
		self._deleteJsonInTable(json, "mail", commit=True)

	def deleteJsonPhone(self, json):
		self._deleteJsonInTable(json, "phone", commit=True)

	def deleteJsonAddress(self, json):
		self._deleteJsonInTable(json, "address", commit=True)

	def deleteJsonStudy(self, json):
		self._deleteJsonInTable(json, "study", commit=True)

	def _insertJsonInTable(self, json ,table, commit=False):
		query = ContactController.INSERT_QUERIES[table]
		args = self._getInsertArgsFromJsonForTable(json, table)
		self.database.cursor.execute(query,args)
		if commit:
			self.database.commit()
		return self.database.cursor.lastrowid

	def _updateJsonInTable(self, json ,table, commit=False):
		query = ContactController.UPDATE_QUERIES[table]
		args = self._getUpdateArgsFromJsonForTable(json, table)
		self.database.cursor.execute(query,args)
		if commit:
			self.database.commit()

	def _deleteJsonInTable(self, json ,table, commit=False):
		query = ContactController.DELETE_QUERIES[table]
		args = self._getDeleteArgsFromJsonForTable(json, table)
		self.database.cursor.execute(query,args)
		if commit:
			self.database.commit()

	def _getInsertArgsFromJsonForTable(self, json, table):
		columns = ContactController.INSERT_COLUMNS[table]
		return tuple([json[col] for col in columns])

	def _getUpdateArgsFromJsonForTable(self, json, table):
		columns = ContactController.UPDATE_COLUMNS[table]
		return tuple([json[col] for col in columns])

	def _getDeleteArgsFromJsonForTable(self, json, table):
		columns = ContactController.DELETE_COLUMNS[table]
		return tuple([json[col] for col in columns])



