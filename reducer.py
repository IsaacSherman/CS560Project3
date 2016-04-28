#!/usr/bin/python

import sys

titleF = open('names', 'r')
titles = {}
for line in titleF:
	k, v = line.split(',')
	titles[k] = v

currentKey = -1

for line in sys.stdin:
	line = line.strip()
	key, value = line.split('|:')

	key = key.strip()
	value = value.strip()

	if currentKey != int(key):
		if currentKey != -1:
			print str(currentKey) + "," + str(pageRank) + '|:' + linksList
		
		pageRank = 0.15/len(titles)
		# print pageRank
		currentKey = int(key)

	if value[0] == '[':
		linksList = value[1:-1]
		# print linksList

	else:
		pageRank = pageRank + 0.85*float(value)
	
	# print pageRank

print str(currentKey) + ',' + str(pageRank) + '|:' + linksList
