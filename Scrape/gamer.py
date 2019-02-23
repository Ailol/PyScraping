import argparse
import sys
import os
import requests
import lxml
from lxml import html
import db
import collections
import pprint

"""	
	Short webscraper that fetches registered teams in telenorligaen @ GAMER.no
"""
session_requests = requests.session()

def print_results(count, count2, team_name):
	print("\n # # # # # # # # # ")
	print(" # "+team_name+"  ")
	print(" # # # # # # # # # \n")
	print(" __BANS__  ")
	pprint.pprint(count)
	print("\n __PICKS__ ")
	pprint.pprint(count2)



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

def get_veto(team_name, team_url):

	url    = team_url
	result = session_requests.get(url, headers = dict(referer = url))
	tree   = html.fromstring(result.content)

	match_list = tree.xpath('//a[contains(@href,"/turneringer/kamp")]/@href')
	pick = []
	ban  = []


	for i in range(len(match_list)):
		vetourl = "https://www.gamer.no" + match_list[i]
		match = session_requests.get(vetourl, headers = dict(referer = vetourl))
		res   = html.fromstring(match.content)
		teamlist = res.xpath('//div[contains(@class, "veto-detail team")]/text()')
		maplist = res.xpath('//div[contains(@class, "veto-detail map")]/text()')

		i = 0
		for t, m in zip(teamlist,maplist):
			if t.strip() == team_name:
				ban.append(m.strip())

			if i == 2:
				pick.append(m.strip())
			i += 1	
		
		
	count = collections.Counter(ban)
	count2 = collections.Counter(pick)

	return print_results(count, count2, team_name)

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
		s = input("1. check how many teams are in \n2. get vetoes of given team \nANSWER:")
		if s == 1:
			DB = get_teams()
			db.create_database(DB)
		else:
			get_veto(args[2], args[3])

		
	except IndexError:
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno)) 



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

	parser.add_argument(
	    'team_name',
	    type=str,
	    help='Enter login username',
	    default='err')
	parser.add_argument(
	    'team_url',
	    type=str,
	    help='Enter password for site',
	    default="err")

	args = parser.parse_args()

	main(args.username, args.password, args.team_name, args.team_url)

