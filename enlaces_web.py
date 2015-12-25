# -*- coding: utf-8 -*-

#script que devolve todos os enlaces de unha páxina web

import re
import urllib2
import sys

def comprobar_enlaces(list):
	lista_webs = []
	for url in list:
		if re.findall("^www.",url[1]) or re.findall("^https?://",url[1]):
			lista_webs.append(url)
	return lista_webs

def enlaces_web(web):
	try:
		web_code = urllib2.urlopen(web).read()
		links = re.findall('(href)="(\S+)"|(src)="(\S+)"',web_code)
		info = [[link[0]+link[2],link[1]+link[3]] for link in links]
		links_salida = []
		for l in info:
			link = l[1]
			if (len(link) > 1) and (link[0] and link[1] == "/"):
				links_salida.append(["http:"+link,l[1]])
			elif link[0] == "/":
				links_salida.append([web+link,l[1]])
			else:
				links_salida.append(l)
		return comprobar_enlaces(links_salida)
	except:
		return False
	
if len(sys.argv) > 1:
	try:
		web = sys.argv[1]
		if not re.findall("^https?://",web):
			web = "http://"+web
		for link in enlaces_web(web):
			print link[0],link[1]
	except:
		print "ERROR"
else:
	print "Falta enlace como argumento"

