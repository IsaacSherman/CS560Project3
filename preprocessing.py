#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')
names = open('names', 'w')
part = open('data0/part-0000', 'w')

count = 0
titles = {}

# make sure that only represented titles are in the 'names' file
for line in f:
	k, v = line.split('|:')

	index, _ = k.split(',')

	if not index in titles:
		count += 1
		titles[index] = count
		names.write(str(index) + ',' + str(count) + '\n')

f.seek(0)

# adjust probabilities and make sure that only represented titles are in value
for line in f:
	k, v = line.split('|:')

	index, _ = k.split(',')
	pr = 1/float(len(titles))

	links = v.split(',')
	outLinks = ''

	for link in links:
		if link in titles:
			outLinks += link + ','

	outLinks += outLinks.strip(',')

	part.write(index + ',' + str(pr) + '|:' + outLinks + '\n')
	outLinks = ''
