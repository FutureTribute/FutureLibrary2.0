"""
Created by: Zasko B.
Creates connection to MYSQL server and cursor object for working with DB
"""

import mysql.connector


user = "root"
password = ""
host = "localhost"
database = "games"

cnx = mysql.connector.connect(user=user, password=password,
                              host=host, database=database)

cursor = cnx.cursor()
