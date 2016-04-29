#!/usr/bin/python

import xml.sax
import sys
import re

def regex(text):
	links = []
	rawLinks = re.findall(r'\[\[(.+?)\]\]', text)
	
	for link in rawLinks:
		# some links have a '|' so try splitting and data is in first
		link = link.split('|')

		# check to see if link is to a File
		if not 'File' in link[0]:
			links.append('_'.join(link[0].encode('ascii', 'ignore').split(' ')))
	
	return links

class parser(xml.sax.ContentHandler):
	def __init__(self, outputFile):
		self.titlesDict = {}
		self.currentLinksListDict = {}
		self.outputFile = open(outputFile, 'w')
		self.titleFlag = False
		self.contentFlag = False
		self.currentTitle = ''
		self.currentContent = ''
		self.currentLinksList = [] 
		self.currentLinksString = ''
		self.initialPR = 0
		self.dataLine = ''

		titles = open('simplewiki-20160305-all-titles', 'r')
		count = 1
		for title in titles:
			self.titlesDict[title.strip()] = count
			count += 1

		self.initialPR = 1/float(len(self.titlesDict))

	def startElement(self, name, attrs):
		# if the name of the flag is one that we are searching for
		if name == 'title':
			self.titleFlag = True

		elif name == 'text':
			self.contentFlag = True

	
	def characters(self, content):
		# if the flag for the tag is set then save the content appropriately
		if self.titleFlag:
			self.currentTitle = '_'.join(content.encode('ascii', 'ignore').split(' '))

		elif self.contentFlag:
			self.currentContent += content

	
	def endElement(self, name):
		# if closing title is found reset flag
		if self.titleFlag:
			self.titleFlag = False
		
		# if closing text is found then process data and emit
		elif self.contentFlag:
			if self.currentTitle in self.titlesDict:
				# if title is in the main list then add it and initialPR to dataLine buffer
				self.dataLine += str(self.titlesDict[self.currentTitle])+','+str(self.initialPR)+'|:'

				# search current content for links
				self.currentLinksList = regex(self.currentContent)

				# add non-redundant, valid links to linksList
				for link in self.currentLinksList:
					if ( not link in self.currentLinksListDict ) and ( link in self.titlesDict ):
						self.currentLinksString += str(self.titlesDict[link])+','
						self.currentLinksListDict[link] = 1
				
				self.currentLinksString = self.currentLinksString.strip(',')
				self.dataLine += self.currentLinksString+'\n'
				self.outputFile.write(self.dataLine)

			self.dataLine = ''
			self.currentTitle = ''
			self.currentContent = ''
			self.currentLinksString = ''
			self.currentLinksList = []
			self.currentLinksListDict = {}
			self.contentFlag = False




if __name__ == "__main__":
	# create a parser
	saxParser = xml.sax.make_parser()

	# set the content handler
	saxParser.setContentHandler(parser('data0/part-00000'))

	# tell the parser which file to parse
	saxParser.parse(open('simplewiki-20160305-pages-articles.xml', 'r'))
