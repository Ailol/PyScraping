import re

def median(lst):
    quotient, remainder = divmod(len(lst), 2)
    if remainder:
        return sorted(lst)[quotient]
    return sum(sorted(lst)[quotient - 1:quotient + 1]) / 2.

l = ['alt="Skill level 1"',
	'alt="Skill level 2"',
	'alt="Skill level 3"',
	'alt="Skill level 4"',
	'alt="Skill level 5"',
	'alt="Skill level 6"',
	'alt="Skill level 7"',
	'alt="Skill level 8"',
	'alt="Skill level 9"',
	'alt="Skill level 10"',
	]


res = []
with open("faceit.html",'r', encoding='utf8') as f:
	lines = f.read().splitlines()
	for line in lines:
		for i in range(10):
			if re.search(l[i], line):
				res.append(l[i])

r= []
for i in range(len(res)):
	lol = res[i]
	r.append(lol[17:18])
	if lol[17:19] == '10':
		r.append(lol[17:19])

r= list(map(int, r))
print("\n\nFaceit average level in team leagues: " ,median(r))
print("\n\n")