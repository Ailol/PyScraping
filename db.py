import sqlite3
import os

def create_database(lol):

	conn = sqlite3.connect('gamer.db')
	c = conn.cursor() 

	c.execute('''create table CS(Team text,date text)''')

	c.executemany("INSERT INTO CS VALUES (?,?)", lol)

	conn.commit()
	conn.close()