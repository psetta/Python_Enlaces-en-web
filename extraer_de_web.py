# -*- coding: utf-8 -*-

import os
import re
import urllib2
import sys
import webbrowser
import itertools

#DEVOLVE TODOS OS ENLACES DE UNHA WEB
def enlaces_web(web,busqueda,tipo):
		#TEXTO DE TODA A WEB
		web_code = urllib2.urlopen(web).read()
		#FILTRAMOS POR TIPO
		if tipo == "href":
			expresion_regular = '(href)="(\S+)"'
			pre_links = re.findall(expresion_regular,web_code)
		elif tipo == "src":
			expresion_regular = '(src)="(\S+)"'
			pre_links = re.findall(expresion_regular,web_code)
		else:
			expresion_regular = '(href)="(\S+)"|(src)="(\S+)"'
			pre_links = re.findall(expresion_regular,web_code)
			pre_links = [[x[0]+x[2],x[1]+x[3]] for x in pre_links]
		#ENGADIMOS O NECESARIO AOS LINKS PARA QUE ESTEAN CORRECTOS
		links_final = []
		for l in pre_links:
			link = l[1]
			if (len(link) > 1) and (link[0] and link[1] == "/"):
				links_final.append([l[0],"http:"+link])
			elif link[0] == "/":
				links_final.append([l[0],web+link])
			elif len(link) > 1:
				links_final.append(l)
		#FILTRAMOS POR BUSQUEDA
		links_salida = []
		if busqueda:
			for l in links_final:
				if re.findall(busqueda,l[1]):
					links_salida.append(l)
		else:
			links_salida = links_final
		#ELIMINAMOS DUPLICADOS
		links_salida.sort()
		links_salida = list(link for link,_ in itertools.groupby(links_salida))
		#DEVOLVEMOS A LISTA DE LINKS
		return links_salida
		
#CREA UNHA WEB CON UNHA TABOA DONDE SE REPRESENTAN OS ENLACES RESULTANTES
def crear_web_datos(web,links):
	html_document = open("datos_enlaces.html","w")
	tags_apertura = "<html>\n<head>\n<title>Datos_Enlaces</title>\n</head>\n"
	tags_style = "<style>\ntable {border-collapse: collapse;}\ntd {padding: 5px;}\n</style>\n"
	tags_body = "<body>\n<h2>"+(web if (len(web) < 100) else web[:150]+"...")+"</h2>\n<table border=1>\n"
	tags_final = "</body>\n</html>"
		
	html_document.write(tags_apertura)
	html_document.write(tags_style)
	html_document.write(tags_body)
	
	for link in links:
		html_document.write('\t<tr><td bgcolor="'+("lightgreen" if link[0]=="src" else "lightblue")+
					'">'+link[0]+"</td><td><a href="+'"'+link[1]+'">'+
					(link[1] if (len(link[1]) < 150) else link[1][:150]+"...")+"</a></td></tr>\n")
	html_document.write("</table>")
	html_document.write(tags_final)
	
	html_document.close()
		
	webbrowser.open("datos_enlaces.html")
	
#DESCARGA O CONTIDO DOS ENLACES
def descargar(dir,links):
	for l in links:
		link = l[1]
		try:
			file_url = urllib2.urlopen(link)
			name_file = link.replace("/","").replace(":","").replace("?","")
			arquivo = file(dir+"/"+name_file,"wb")
			arquivo.write(file_url.read())
			arquivo.close()
			print "Descargado "+link
		except:
			print "Error - Non foi posible descargar: "+link
			
#VER WEBS DENTRO DO MESMO DOMINIO
def next_in_web(web,links):
	web = web.split("/")
	web = web[:3]
	web = "/".join(web)
	next_in_webs = []
	for l in links:
		if l[0] == "href":
			link = l[1]
			if re.findall("^"+web+".+"+".html$",link) and not re.findall("#",link):
				next_in_webs.append(link)
	print "#"*20
	print "domain: "+web
	for n in next_in_webs:
		print "web: "+n
	print "#"*20
	
#LEE OS ARGUMENTOS QUE SE LLE PASA AO SCRIPT E EJECUTA AS FUNCIONS CORRESPONDENTES
def leer_argumentos(args):
	args_enlaces_web = args[2:] + [None for x in range(5-len(args))]
	web = args_enlaces_web[0]
	if not re.findall("^https?://",web):
		web = "http://"+web
		args_enlaces_web[0] = web
	#REPRESENTAR ARGUMENTOS
	print "salida:\t\t"+str(args[1])
	print "web:\t\t"+str(args_enlaces_web[0])
	print "busqueda:\t"+str(args_enlaces_web[1])
	print "tipo:\t\t"+str(args_enlaces_web[2])
	print
	enlaces = enlaces_web(*args_enlaces_web)
	next_in_web(web,enlaces)
	print
	#TIPO DE SALIDA
	tipo_salida = args[1]
	if tipo_salida in ["0","terminal","consola"]:
		for l in enlaces:
			print l[0]+"\t"+l[1]
	elif tipo_salida in ["1","web","html"]:
		crear_web_datos(web,enlaces)
	elif tipo_salida in ["2","descarga","download"]:
		dir_name = web+str(args_enlaces_web[1])+str(args_enlaces_web[2])
		dir_name = dir_name.replace("/","").replace(":","").replace("?","")
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		descargar(dir_name,enlaces)
		
def main():
	leer_argumentos(sys.argv)
		
if __name__ == "__main__":
    main()

