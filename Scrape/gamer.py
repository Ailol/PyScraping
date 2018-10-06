import argparse
import sys
import os
import requests
import lxml
from lxml import html
import db

"""	
	Short webscraper that fetches registered teams in telenorligaen @ GAMER.no
"""
session_requests = requests.session()

def login(username, password): 
	payload = {
		"email": username,
		"password": password,
		"_token": "_token"
	}

	url  = "https://auth.tumedia.no/logg-inn"
	result 	= session_requests.get(url)
	tree 	= html.fromstring(result.text)

	authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]
	result = session_requests.post(url, data = payload, headers = dict(referer=url))

	## FIX: sending value back
	if result.status_code == 200:
		pass
	else:
		raise IndexError


def get_teams():
	"""
		Creates list of teams and signup dates, returns a tuple [(TEAM, SIGNUP TIME)].
	"""

	url = "https://www.gamer.no/turneringer/telenorligaen-counter-strike-go-hosten-2018/4950/deltakere/"
	result = session_requests.get(url, headers = dict(referer = url))
	tree   = html.fromstring(result.content)

	team_list = (tree.xpath('.//span[contains(@class, "signup-name")]/a/text()'))
	signup_list = (tree.xpath('.//span[contains(@class, "signup-time")]/text()'))

	return list(zip(team_list, signup_list))

def main(*args):
	"""
		Tries to query login and fetch teams, raises 
		indexing error if login failed. 
	"""

	try:
		login(args[0],args[1])
		DB = get_teams()
	except IndexError:
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)) 

	db.create_database(DB)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
	    description='Simple webscraper for GAMER.no,\n args: username(EMAIL), password')
	parser.add_argument(
	    'username',
	    type=str,
	    help='Enter login username',
	    default='err')
	parser.add_argument(
	    'password',
	    type=str,
	    help='Enter password for site',
	    default="err")

	args = parser.parse_args()

	main(args.username, args.password)





