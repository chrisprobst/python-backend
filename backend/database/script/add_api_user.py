import logging
import os
import time

from passlib.hash import pbkdf2_sha256

from backend.database import Database

db = Database.Database("../../../myDatabase.db", logging.getLogger("Test"))
username = raw_input("Username: ")
password = raw_input("Password: ")
print "Generate salt..."
salt = os.urandom(256).encode('hex')
salted_password = salt+password
print "Compute passhash..."
hashed_password = pbkdf2_sha256.encrypt(salted_password, rounds=400000)
print "Generated passhash:", hashed_password
print "Insert into database..."
query = "INSERT INTO users (username, passhash, salt, created) VALUES (?,?,?,?);"
args = (
	username,
	hashed_password,
	salt,
	time.time()
)
db.cursor.execute(query, args)
db.commit()
print "Done."