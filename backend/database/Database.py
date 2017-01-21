import sqlite3

class Database(object):

	def __init__(self, path, debug=False, logger=None):
		self.debug = debug
		self.logger = logger
		self.connection = sqlite3.connect(path)
		self.cursor = self.connection.cursor()
		self.createTables()

	def createTables(self):
		self.cursor.execute(

			"""CREATE TABLE IF NOT EXISTS `users` (
			`username` TEXT PRIMARY KEY,
			`passhash` TEXT,
			`salt` TEXT,
			`created` DATE DEFAULT CURRENT_TIMESTAMP

		)""")
		self.cursor.execute(

			"""CREATE TABLE IF NOT EXISTS `api_tokens` (
			`username` TEXT,
			`api_token` TEXT,
			PRIMARY KEY (username, api_token)

		)""")

	def commit(self):
		return self.connection.commit()

	def getSingleValueByQuery(self, query, args=None):
		if args:
			self.cursor.execute(query,args)
		else:
			self.cursor.execute(query)
		result = self.cursor.fetchone()
		if not result:
			if self.debug:
				msg = "Query '{query}' with args '{args}' didnt return any value".format(query=query, args=args)
				self.logger.warning(msg)
			return None
		else:
			return result[0]


if __name__ == "__main__":
	db = Database()
	