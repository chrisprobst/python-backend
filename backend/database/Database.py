import sqlite3

class Database(object):

	def __init__(self, path):
		self.connection = sqlite3.connect(path)
		self.cursor = self.connection.cursor()
		self.createTables()

	def createTables(self):
		# self.cursor.execute( CREATE ALL TABLES NEEDED )
		pass

	def commit(self):
		return self.connection.commit()


if __name__ == "__main__":
	db = Database()