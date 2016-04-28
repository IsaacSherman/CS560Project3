#!/usr/bin/python

import sys

titleF = open('names', 'r')
titles = {}
for line in titleF:
	k, v = line.split(',')
	titles[k] = v


for line in sys.stdin:
	line = line.strip()
	
	key, value = line.split("|:")

	index, pr = key.split(',')
	pr = float(pr)

	linksList = value.split(',')

	# if page is dangling
	if not value:
		for key in titles:
			key = key.strip()
			print(key + '|:' + str(pr/len(titles)))
	
	# if page is NOT dangling
	else:
		for key in linksList:
			key = key.strip()
			print (key + '|:' + str(pr/len(linksList)))

	# finally emit self
	print (index + "|:" + '[' + value + ']') #PICK BACK UP HERE!
