import os
import time

from passlib.hash import pbkdf2_sha256

import Database

db = Database.Database("../../myDatabase.db")
username = raw_input("Username: ")
password = raw_input("Password: ")
salt = os.urandom(256).encode('hex')
salted_password = salt+password
hashed_password = pbkdf2_sha256.encrypt(salted_password, rounds=400000)
print "Hashed and salted password:", hashed_password

query = "INSERT INTO users (username, passhash, salt, created) VALUES (?,?,?,?);"
args = (
	username,
	hashed_password,
	salt,
	time.time()
)
db.cursor.execute(query, args)
db.commit()