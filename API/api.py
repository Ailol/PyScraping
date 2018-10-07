import json
import requests as req
from pprint import pprint

debug = "Succeed"

"""
	Input server key as ua
"""
srv_key = "Bearer 329ec7d1-dd71-467b-a6ff-f735743b8aa7"

main_url = 'https://open.faceit.com/data/v4/championships/3ae0eb6d-b54a-4fd2-9307-e5155c20e430'
url2 = 'https://open.faceit.com/data/v4/championships/3ae0eb6d-b54a-4fd2-9307-e5155c20e430/subscriptions?offset='

def search(listt, key, val):
    for item in listt:
        if item[key] == val:
            return item

def get_current_subs():

	return json.loads((get(main_url).content).decode('utf-8')).get('current_subscriptions')

def _decode_dict(a_dict):
    try: return a_dict[id]
    except KeyError: pass
    return a_dict		


def get(url, params=None):
	"""
		Get response for data, returns a request.get
		Param set to NULL if not given.

	"""

	headers = {
	    'accept': 'application/json',
	    'Authorization': srv_key,
	}

	if params:
		return req.get(url, headers=headers, params=params)

	else:
		return req.get(url, headers=headers)

def get_details(data, *args):
	"""
		create regex pattern to match key,value
	"""
	pass



def get_teams(url, num_teams=None, dump=None):

	i = 0
	data = []

	if not num_teams:
		num_teams = get_current_subs()

	if dump:
		with open('data.txt', 'w', encoding='utf-8') as f:
			for i in range(0, num_teams , 10):
				url2 = (url + str(i) + '&limit=10')
				data = json.loads((get(url2).content).decode('utf-8'))
				json.dump(data, f, sort_keys = True, indent = 4, ensure_ascii = False)
	else:
		for i in range(0, num_teams , 20):
			url2 = (url + str(i) + '&limit=20')
			data = (get(url2).content).decode('utf-8')
			
			print(i)
	return json.loads(data, object_hook=_decode_dict)

def main():
	"""
		name(team)
		nickname
		country
		skill_level

	"""

	param = (('expanded','game'),)

	print(get_current_subs())
	data = get_teams(url2, 50)
	
if __name__ == "__main__":
	main()
