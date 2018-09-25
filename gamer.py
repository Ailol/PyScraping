
import argparse
import os
import requests
import lxml
from lxml import html

"""	
	Short webscraper that fetches registered players in telenorligaen @ GAMER.no
"""
session_requests = requests.session()

def login(username, password, token, url):

	payload = {
		"email": username,
		"password": password,
		"_token": token
	}

	result 	= session_requests.get(url)
	tree 	= html.fromstring(result.text)

	authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]

	result = session_requests.post(url, data = payload, headers = dict(referer=url))

	if result.status_code == 200:
		print("Logged inn!")
	else:
		print("Something went wrong with login. Code: " + str(result))


def get_list():

	url = "https://www.gamer.no/turneringer/telenorligaen-counter-strike-go-hosten-2018/4950/deltakere/"
	result = session_requests.get(url, headers = dict(referer = url))
	tree   = html.fromstring(result.content)

	players = tree.xpath("//ul[@class='signup-name']/ul/text()")
	print(players)
	tot_players = []
	for name in players:
		tot_players.append(name)

	print(tot_players)


def main(*args):

	try:
		login(args[0],args[1],args[2],args[3])
	except BaseException:
		raise ValueError

	get_list()

if __name__ == "__main__":

	parser = argparse.ArgumentParser(
	    description='Simple webscraper for given urls,\n args: username, password, login url, login token')
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
	parser.add_argument(
	    'URL',
	    type=str,
	    help='Enter login url (www.google.com/login)',
	    default="err")
	parser.add_argument(
	    'token',
	    type=str,
	    help='<<inspect>> login element',
	    default="err")

	args = parser.parse_args()

	main(args.username, args.password, args.token, args.URL)






