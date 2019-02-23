import sqlite3
from sqlite3 import Error
import os

def create_database(lol):

	conn = sqlite3.connect('gamer.db')
	c = conn.cursor() 
	try:
		c.execute("create table "+ input("Name of database? :")+ "(Team text,date text)")
		c.executemany("INSERT INTO CS VALUES (?,?)", lol)
		print("Database created!")
	except Error as e:
		print("Already exists-> error code: ",e)
		exit()

	conn.commit()
	conn.close()
