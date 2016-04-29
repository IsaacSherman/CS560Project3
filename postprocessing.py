#!/usr/bin/python

f = open('part-00000', 'r')
names = open(sys.argv[1], 'r')

count = 1
titles = {}

for name in names:
	titles[count] = name
	count += 1

for line in f:
	key, _ = line.strip().split('|:')

	index, pr = key.strip().split(',')

	print pr + ' , ' + str(titles[int(index)])
