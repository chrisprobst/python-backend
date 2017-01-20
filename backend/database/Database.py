import sqlite3

class Database(object):

	def __init__(self, path):
		self.connection = sqlite3.connect(path)
		self.cursor = self.connection.cursor()
		self.createTables()

	def createTables(self):
		# self.cursor.execute( CREATE ALL TABLES NEEDED )
		pass
		self.cursor.execute(

			"""CREATE TABLE IF NOT EXISTS `users` (
			`username` TEXT PRIMARY KEY,
			`passhash` TEXT,
			`salt` TEXT,
			`created_at` DATE DEFAULT CURRENT_TIMESTAMP

		)""")

	def commit(self):
		return self.connection.commit()


if __name__ == "__main__":
	db = Database()