# -*- coding: utf-8 -*-

#script que devolve todos os enlaces de unha páxina web

import re
import urllib2
import sys
import webbrowser
import itertools

def comprobar_enlaces(list):
	lista_webs = []
	for url in list:
		if re.findall("^www.",url[0]) or re.findall("^https?://",url[0]):
			lista_webs.append(url)
	return lista_webs

def enlaces_web(web):
	try:
		web_code = urllib2.urlopen(web).read()
		links = re.findall('(href)="(\S+)"|(src)="(\S+)"',web_code)
		return [[link[1]+link[3],link[0]+link[2]] for link in links]
	except:
		return False
	
if len(sys.argv) > 1:

	web = sys.argv[1]
	total_links = enlaces_web(web)
	links = []
	
	#FILTRAMOS E CORREXIMOS URLs
	
	for l in total_links:
		link = l[0]
		if (len(link) > 1) and (link[0] and link[1] == "/"):
			links.append(["http:"+link,l[1]])
		elif link[0] == "/":
			links.append([web+link,l[1]])
		else:
			links.append(l)
			
	links.sort()
	links = list(links for links,_ in itertools.groupby(links))
	
	links = comprobar_enlaces(links)
		
	html_document = open("datos_enlaces.html","w")
	tags_apertura = "<html>\n<head>\n<title>Datos_Enlaces</title>\n</head>\n"
	tags_style = "<style>\ntable {border-collapse: collapse;}\ntd {padding: 5px;}\n</style>\n"
	tags_body = "<body>\n<h2>"+(web if (len(web) < 100) else web[:150]+"...")+"</h2>\n<table border=1>\n"
	tags_final = "</body>\n</html>"
		
	html_document.write(tags_apertura)
	html_document.write(tags_style)
	html_document.write(tags_body)
	for link in links:
		html_document.write('\t<tr><td bgcolor="'+("lightgreen" if link[1]=="src" else "lightblue")+
					'">'+link[1]+"</td><td><a href="+'"'+link[0]+'">'+
					(link[0] if (len(link[0]) < 100) else link[0][:150]+"...")+"</a></td></tr>\n")
	html_document.write("</table>")
	html_document.write(tags_final)
		
	webbrowser.open("datos_enlaces.html")
	
else:
	print "Falta enlace como argumento"