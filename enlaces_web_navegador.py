# -*- coding: utf-8 -*-

#script que devolve todos os enlaces de unha páxina web

import re
import urllib2
import sys
import webbrowser

def enlaces_web(web):
	try:
		web_code = urllib2.urlopen(web).read()
		links = re.findall("((w{3}\.|https?://)(w{3}\.)?\w+\.\w{2,3}(\s)?(\.\w{2,3})?)",web_code)
		return links
	except:
		return False
	
if len(sys.argv) > 1:

	web = sys.argv[1]
	total_links = enlaces_web(web)
	links = [x[0] for x in total_links]
	links = set(links)
		
	html_document = open("datos_enlaces.html","w")
	tags_apertura = "<html>\n<head>\n<title>Datos_Enlaces</title>\n</head>\n"
	tags_style = "<style>\ntable {border-collapse: collapse;}\n</style>\n"
	tags_body = "<body>\n<h2>"+web+"</h2>\n<table border=1>\n"
	tags_final = "</body>\n</html>"
		
	html_document.write(tags_apertura)
	html_document.write(tags_style)
	html_document.write(tags_body)
	for link in links:
		html_document.write("\t<tr><td><a href="+'"'+link+'">'+link+"</a></td></tr>\n")
	html_document.write("</table>")
	html_document.write(tags_final)
		
	webbrowser.open("datos_enlaces.html")
	
else:
	print "Falta enlace como argumento"