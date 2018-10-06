import argparse
import sys
import os
import requests
import lxml
from lxml import html

"""	
	Short webscraper that fetches registered teams in telenorligaen @ GAMER.no
"""
session_requests = requests.session()

def login(username, password): 
	payload = {
		"login_email": username,
		"login_password": password,
		"recaptcha-token": "recaptcha-token"
	}

	url  = "https://www.faceit.com/en/login"
	result 	= session_requests.get(url)
	tree 	= html.fromstring(result.text) 

	authenticity_token = list(set(tree.xpath("//input[@name='recaptcha-token']/@value")))
	result = session_requests.post(url, data = payload, headers = dict(referer=url))

	## FIX: sending value back
	if result.status_code == 200:
		print("OK")
	else:
		print(result.status_code)


def get_teams() :
	"""
		Creates list of teams and signup dates, returns a tuple [(TEAM, SIGNUP TIME)].
	"""

	url = "https://www.faceit.com/en/championship/3ae0eb6d-b54a-4fd2-9307-e5155c20e430/EU%20WINNERS%20League%20-%20Starter%20Division/teams"
	result = session_requests.get(url, headers = dict(referer = url))
	tree   = html.fromstring(result.content)

	team_list = (tree.xpath('.//span[contains(@class, "subscription.joinSkillLevel")]/a/text()'))
#	signup_list = (tree.xpath('.//span[contains(@class, "signup-time")]/text()'))
	return list(zip(team_list))

#	return list(zip(team_list, signup_list))

def main(*args):
	"""
		Tries to query login and fetch teams, raises 
		indexing error if login failed. 
	"""
	DB = []

	login(args[0],args[1])
	DB = get_teams()
	
	print(DB)

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





