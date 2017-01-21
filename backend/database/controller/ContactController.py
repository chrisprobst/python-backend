class ContactController(object):

	# Set fields that will be inserted into table (note: this is important because
	# there might exist fields like the ID that are not inserted manually)
	COLUMNS = {
		"contact": ("prefix", "first_name", "last_name", "birth_date", "comment"),
		"mail": ("contact_id", "description", "address"),
		"phone": ("contact_id", "description", "number"),
		"address": ("contact_id", "description", "street", "number", "addr_extra", "postal", "city"),
		"study": ("contact_id", "status", "school", "course", "start", "end", "focus", "degree")
	}

	QUERIES = {
		"contact": "INSERT INTO `contact` (prefix, first_name, last_name, birth_date, comment) VALUES (?,?,?,?,?);",
		"mail": "INSERT INTO `mail` (contact_id, description, address) VALUES (?,?,?);",
		"phone": "INSERT INTO `phone` (contact_id, description, number) VALUES (?,?,?);",
		"address": "INSERT INTO `address` (contact_id, description, street, number, addr_extra, postal, city) VALUES (?,?,?,?,?,?,?);",
		"study": "INSERT INTO `study` (contact_id, status, school, course, start, end, focus, degree) VALUES (?,?,?,?,?,?,?,?);"
	}

	def __init__(self, database):
		self.database = database

	def insertJsonContact(self, json):
		return self._insertJsonInTable(json, "contact")

	def insertJsonMail(self, json):
		return self._insertJsonInTable(json, "mail")

	def insertJsonPhone(self, json):
		return self._insertJsonInTable(json, "phone")

	def insertJsonAddress(self, json):
		return self._insertJsonInTable(json, "address")

	def insertJsonStudy(self, json):
		return self._insertJsonInTable(json, "study")

	def _insertJsonInTable(self, json ,table):
		query = ContactController.QUERIES[table]
		args = self._getDataTupleFromJsonForTable(json, table)
		self.database.cursor.execute(query,args)
		self.database.commit()
		return self.database.cursor.lastrowid

	def _getDataTupleFromJsonForTable(self, json, table):
		columns = ContactController.COLUMNS[table]
		print columns
		print json
		return tuple([json[col] for col in columns])


