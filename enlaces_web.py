# -*- coding: utf-8 -*-

#script que devolve todos os enlaces de unha páxina web

import re
import urllib2
import sys

def enlaces_web(web):
	try:
		web_code = urllib2.urlopen(web).read()
		links = re.findall("((w{3}\.|https?://)(w{3}\.)?\w+\.\w{2,3}(\s)?(\.\w{2,3})?)",web_code)
		return links
	except:
		return False
	
if len(sys.argv) > 1:
	try:
		for link in enlaces_web(sys.argv[1]):
			print link[0]
	except:
		print "ERROR"
else:
	print "Falta enlace como argumento"

