#! /usr/bin/env python

'''Query IMDB for movie information and output to terminal'''


import os
import urllib2
#import cPickle
import sys
import re
import textwrap
import time

import bs4
from bs4 import BeautifulSoup

__author__ = "Tom"
__copyright__ = "2013"
__credits__ = "Tom"
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Tom"
__email__ = "tom@drakero.com"
__status__ = "Prototype"

#Start program

imbd = "http://www.imdb.com/find?q={}&s=all"
check = sys.argv[1]
debug = False

#Debug mode!
if len(sys.argv) > 2:
	if sys.argv[2] == "-d":
		debug = True
		print "Debug mode on."
		with open('debug.log', 'w') as f:
			f.write('*'*60)
			f.write('Debug for ' + sys.argv[1] + ' on ' + time.asctime())

def getDirectory():
	''' not complete'''
	temp = 	os.popen('ls <directory>').read().split('\n')
	temp.pop()
	return temp

def conformString(stz):
	'''Used in getMovieData() to check string to prevent an 404 or other errors for non URL encoded chars '''
	#To Do: do a more intensive string fix for html request	(REMOVE ALL SPECIAL CHARS AND NON URL ENCODED CHARS)
	#input.append(data.lower().replace("."," ").replace(" ","+").replace('avi'or'mp4'or'wmv'or'xvid'or'cam'or'TS'or'dvdrip',""))
	temp = stz.strip().lower().replace(" ","+")
	if debug:
		with open('debug.log','ab+') as f:
			f.write("\n\nconformString() returns: " +  temp)
	return temp

def getAll(data):
	'''Formats HTML data from getMovieData() to a dictionary with all collected values'''
	soup = BeautifulSoup(data)	
	plot_ = None
	run_ = None
	gen_ = None
	cas_ = None
	rel_ = None
	rat_ = None
	dir_ = None
	sim_ = None
	tempDet = soup.find_all('h1')
	title = tempDet[0].text.encode('ascii','replace')
	for x in tempDet:
		if x.text=="Plot Summary":
			plot_ = x
		elif x.text == "Run time":
			run_ = x
		elif x.text == 'Genre':
			gen_ = x
		elif x.text == 'Top Billed Cast':
			cas_ = x
		elif x.text == 'Release Date':
			rel_ = x
		elif x.text == 'Rated':
			rat_ = x
		elif x.text == 'Director':
			dir_ = x
		elif x.text == 'More Like This':
			sim_ = x
		else:
			pass
	rating = rat_.parent.p.text.encode('ascii','replace')
	descrip = tempDet[0].parent.p.text.encode('ascii','replace')
	cast = [x.text.encode('ascii','replace') for x in cas_.parent.findAll('a')][:-1]
	genre = gen_.parent.p.text.encode('ascii','replace')
	runtime = run_.parent.p.text.encode('ascii','replace')
	summary = plot_.parent.p.text.strip().replace('Full Summary','').strip().encode('ascii','replace')
	runtime = run_.parent.p.text.encode('ascii','replace')
	similar =  [x.text.encode('ascii','replace') for x in sim_.parent.findAll('a')][:-1]
	director =  dir_.parent.p.text.strip().encode('ascii','replace')
	release = rel_.parent.p.text.encode('ascii','replace')
	#rated = re.findall(r'(.*?)/',soup.findAll('p','votes','strong')[0].text)[0] + " / 10"
	userRated = soup.findAll('p', 'votes')[0].strong.text.encode('ascii','replace')
	tempDict = {"rating" : rating,"title" : title, 'descrip' : descrip, 'cast' : cast, 'genre'\
 : genre, 'release' : release, 'summary' : summary,'userRated' : userRated, 'runtime' : runtime, 'similar' : similar, 'director' : director}
	
	return tempDict

def output(dicz):
	'''Prints a terminal output of data collected on a movie'''
	print "{title:*^60}\n{descrip:^60}\n{rating:^60}".format(**dicz)
	print '\n{}{release:<20}{:>20}{runtime}'.format('Released: ','Runtime: ', **dicz)
	print '{:^60}'.format("Cast")
	for x in range(0,len(dicz.get('cast'))-1,2):
		print '{:^30}{:^30}'.format(dicz.get('cast')[x],dicz.get('cast')[x+1])
	print '\nGenre: {genre}\n'.format(**dicz)	
	print textwrap.fill('Summary: {summary}'.format(**dicz),60)
	print '{:*^60}'.format('')

def getMovieData(movie):
	'''Returns HTML movie data for the input string'''
	#To do: Error checking on if movie is not found - or bad request...
	temp = urllib2.urlopen(imbd.format(conformString(check))).read()
	temp = re.findall(r'<tr class="findResult odd"> <td class="primary_photo"> <a href="(.+?)\"',temp)[0]
	##temp = urllib2.urlopen('http://www.imdb.com{}'.format(temp)).read()
	url = 'http://www.imdb.com{}'.format(temp)
	ua_string = 'BlackBerry9700/5.0.0.862 Profile/MIDP-2.1 Configuration/CLDC-1.1 VendorID/331 UNTRUSTED/1.0 3gpp-gba'
	headers = {'User-Agent' : ua_string}
	req = urllib2.Request(url,'',headers)
	temp = urllib2.urlopen(req).read()
	if debug:
		with open('debug.log','ab+') as f:
			f.write("\n\n"+temp)
	return temp

if __name__=='__main__':
	output(getAll(getMovieData(check)))
