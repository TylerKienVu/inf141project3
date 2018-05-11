"""This script will setup the tables for the index. Make sure to setup
a database and to change the credentials in the connect function."""

import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="mTigerl8855!",
                     db="inf141")

# Create a Cursor object to execute queries.
cur = db.cursor()

# Create tables in database
cur.execute("")


