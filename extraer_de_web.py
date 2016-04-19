# -*- coding: utf-8 -*-

import os
import re
import urllib2
import sys
import webbrowser
import itertools

#OPCIONS##############################

tipos_web_a_procesar = ["html"]
multiproceso = True
fios_maximos = 20
urlopen_timeout = 20

######################################

#SE O MULTIPROCESO ESTA HABILITADO
if multiproceso:

	import threading
	
	semaforo_fios_descarga = threading.BoundedSemaphore(fios_maximos)
	semaforo_fios_proc_web = threading.BoundedSemaphore(fios_maximos)
	
	class Fio_descarga(threading.Thread):
		def __init__(self,link,dir):
			super(Fio_descarga, self).__init__()
			self.link = link
			self.dir = dir
		def run(self):
			semaforo_fios_descarga.acquire()
			link_fio = self.link
			dir_fio = self.dir
			try:
				file_url = urllib2.urlopen(link_fio)
				name_file = link_fio.replace("/","").replace(":","").replace("?","").replace("|","")
				arquivo = file(dir_fio+"/"+name_file,"wb")
				arquivo.write(file_url.read())
				arquivo.close()
				try:
					self.link = link_fio.decode("utf8")
				except:
					pass
				#print "Descargado "+link_fio
			except:	
				None
				#print "Error - Non foi posible descargar: "+link_fio
			semaforo_fios_descarga.release()
			
	class Fio_procesar_web(threading.Thread):
		def __init__(self,args):
			super(Fio_procesar_web, self).__init__()
			self.args = args
			self.enlaces = 0
		def run(self):
			semaforo_fios_proc_web.acquire()
			self.enlaces = enlaces_web(*self.args)
			semaforo_fios_proc_web.release()
			
####

webs_mesmo_dominio = []
webs_mesmo_dominio_extraidas = []
webs_de_salto = []

#DEVOLVE TODOS OS ENLACES DE UNHA WEB
def enlaces_web(web,busqueda,tipo,recur):
	global webs_mesmo_dominio
	global webs_mesmo_dominio_extraidas
	global webs_de_salto
	
	#TEXTO DE TODA A WEB
	if not multiproceso:
		print "## WEB:\t"+web
	try:
		url_info = urllib2.urlopen(web, timeout=urlopen_timeout)
		tipo_web = url_info.info()["Content-Type"]
		if not multiproceso:
			print "::TIPO:\t"+tipo_web
		web_code = url_info.read()
		web_code = web_code.replace("'",'"')
	except:
		if not multiproceso:	
			print "ERROR - Imposible conectar"
			print
		return []
	procesar = False
	for tipo in tipos_web_a_procesar:
		if tipo in tipo_web:
			procesar = True
			
	if procesar:
		#DIVERSA FORMA DE PROCESAR SEGUN SE BUSQUE UNHA WEB OU TODAS AS DO DOMINIO
		if recur in ["1","True","total","t"]:
			expresion_regular = '(href)="(\S+)"|(src)="(\S+)"'
			pre_links = re.findall(expresion_regular,web_code)
			pre_links = [[x[0]+x[2],x[1]+x[3]] for x in pre_links]
			#CORREXIMOS LINKS
			links_correxidos = correxir_links(web,pre_links)
			#WEBS DO MESMO DOMINIO
			if recur in ["total","t"]:
				webs_dominio = next_in_web(web,links_correxidos,1)
			else:
				webs_dominio = next_in_web(web,links_correxidos,0)
			#FILTRAMOS AS QUE ESTAN REPETIDAS
			webs_mesmo_dominio = webs_mesmo_dominio + [x for x in webs_dominio 
										if x not in webs_mesmo_dominio_extraidas]
			webs_mesmo_dominio = list(set(webs_mesmo_dominio))
			if not multiproceso:
				if webs_de_salto:
					print "## Procesada. Restantes: "+str(len(webs_de_salto))
					print
				else:
					print "## Procesada."
					print
			#FILTRAMOS AGORA POR TIPO
			if tipo in ["href","src"]:
				links_correxidos = [x for x in links_correxidos if x[0] == tipo]
				
		else:
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
			#CORREXIMOS LINKS
			links_correxidos = correxir_links(web,pre_links)
			
		#FILTRAMOS POR BUSQUEDA
		links_salida = []
		if busqueda and not busqueda in ["","0","None"]:
			for l in links_correxidos:
				if re.findall(busqueda,l[1]):
					links_salida.append(l)
		else:
			links_salida = links_correxidos
		#ELIMINAMOS DUPLICADOS
		links_salida.sort()
		links_salida = list(link for link,_ in itertools.groupby(links_salida))
		#DEVOLVEMOS A LISTA DE LINKS
		return links_salida
		
	else:
		if not multiproceso:
			print ("## Este link non corresponde a "+str(tipos_web_a_procesar)+"."+
				" Non se procesa. Restantes: "+str(len(webs_de_salto)))
			print
		return []
		
#CREA UNHA WEB CON UNHA TABOA DONDE SE REPRESENTAN OS ENLACES RESULTANTES
def crear_web_datos(web,links):
	nome_web = web.split("/")[2].replace(":","").replace("?","")
	nome_html = "datos_enlaces_"+nome_web+".html"
	html_document = open(nome_html,"w")
	tags_apertura = "<html>\n<head>\n<meta charset="+"UTF-8"+">\n<title>Datos_Enlaces</title>\n</head>\n"
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
		
	webbrowser.open(nome_html)
	
#CORREXIR LINKS
def correxir_links(web,links):
	links_salida = []
	for l in links:
		link = l[1]
		if link[len(link)-1] in ['"', "'"]:
			link = link[:len(link)-1]
		if (len(link) > 1) and (link[0] and link[1] == "/"):
			links_salida.append([l[0],"http:"+link])
		elif link[0] == "/":
			links_salida.append([l[0],web+link])
		elif len(link) > 1:
			links_salida.append(l)
	return links_salida
	
#DESCARGA O CONTIDO DOS ENLACES
def descargar(dir,links):

	if multiproceso:
		print "Descargando "+str(len(links))+" arquivos..."
		Procesos_descarga = []
		#EXECUTAMOS OS PROCESOS
		for l in links:
			link = l[1]
			Procesos_descarga.append(Fio_descarga(link,dir))
			try:
				Procesos_descarga[-1].start()
			except:
				del Procesos_descarga[-1]
		for fio in Procesos_descarga:
			fio.join()
			
	else:
		total = len(links)
		for l in links:
			link = l[1]
			try:
				file_url = urllib2.urlopen(link)
				name_file = link.replace("/","").replace(":","").replace("?","").replace("|","")
				arquivo = file(dir+"/"+name_file,"wb")
				arquivo.write(file_url.read())
				arquivo.close()
				try:
					link = link.decode("utf8")
				except:
					pass
				print str(total)+" - "+"Descargado "+link
			except:
				print str(total)+" - "+"Error - Non foi posible descargar: "+link
			total -= 1
			
#VER WEBS DENTRO DO MESMO DOMINIO
def next_in_web(web,links,mode):
	web = web.split("/")
	web = web[:3]
	web = "/".join(web)
	next_in_webs = []
	if mode:
		expre_regular = "^"+web+".+"
	else:
		expre_regular = "^"+web+".+"+".html$"
	for l in links:
		if l[0] == "href":
			link = l[1]
			if (re.findall(expre_regular,link) and not re.findall("#",link)):
				next_in_webs.append(link)
	return next_in_webs

max_saltos = 0
enlaces = []

#LEE OS ARGUMENTOS QUE SE LLE PASA AO SCRIPT E EJECUTA AS FUNCIONS CORRESPONDENTES
def leer_argumentos(args):
	global max_saltos
	global enlaces
	global webs_de_salto
	
	if len(args) > 1 and args[1] in ["-h","-help","/?","h","help"]:
		print "::AXUDA"
		print
		print ">> salida:"
		print "\t0 -> terminal"
		print "\t1 -> web"
		print "\t2 -> descarga"
		print
		print ">> web:"
		print "\tlink da web da que queremos extraer datos"
		print
		print ">> busqueda:"
		print "\t0 -> Non fai ningunha busqueda"
		print "\te -> e = expresion regular que queremos buscar. Exemplo: .pdf$"
		print
		print ">> etiqueta:"
		print "\t0 -> devolve todos os links"
		print "\thref -> devolve links coa etiqueta href"
		print "\tsrc -> devolve links coa etiqueta src"
		print
		print ">> recursiva:"
		print "\t0 -> solo busca na web indicada"
		print "\t1 -> busca na web indicada e nos enlaces desta que rematen en .html"
		print "\tt -> busca na web indicada e en todos os enlaces de esta. Sen importar extension"
		print
		print ">> maximo de saltos: (solo funciona se 'recursiva' esta activado)"
		print "\t0 -> sen limite"
		print "\tx -> x = numero. despois de x saltos xa non fai busquedas"
		return 0
	
	elif len(args) > 2:
		args_enlaces_web = args[2:] + [0 for x in range(7-len(args))]
		web = args_enlaces_web[0]
		if not re.findall("^https?://",web):
			web = "http://"+web
			args_enlaces_web[0] = web
		#REPRESENTAR ARGUMENTOS
		tipo_salida = args[1]
		print "salida:\t\t"+str(tipo_salida)
		print "web:\t\t"+str(args_enlaces_web[0])
		print "busqueda:\t"+str(args_enlaces_web[1])
		print "etiqueta:\t"+str(args_enlaces_web[2])
		print "recursiva:\t"+str(args_enlaces_web[3])
		print "n de saltos:\t"+str(args_enlaces_web[4])
		print
	
	else:
		#PEDIR ARGUMENTOS POR CONSOLA
		print "Para axuda: -h ou -help"
		print
		tipo_salida = raw_input("salida: ")
		web = raw_input("web: ")
		busqueda = raw_input("busqueda: ")
		etiqueta = raw_input("etiqueta: ")
		all = raw_input("recursiva: ")
		max_saltos = raw_input("maximo de saltos: ")
		try:
			max_saltos = int(max_saltos)
		except:
			max_saltos = 1
		args_enlaces_web = [web,busqueda,etiqueta,all]
		web = args_enlaces_web[0]
		if not re.findall("^https?://",web):
			web = "http://"+web
			args_enlaces_web[0] = web
		print
		
	#SI QUEREMOS TODAS AS WEBS DO DOMINIO
	if len(args_enlaces_web) > 4:
		max_saltos = int(args_enlaces_web[4])
		args_enlaces_web = args_enlaces_web[:4]
		
	if args_enlaces_web[3] in ["1","True","total", "t"]:
		webs_mesmo_dominio.append(web)
		web_a_extraer = webs_mesmo_dominio[0]
		args_enlaces_web[0] = web_a_extraer	
		
		salto = 0
		while (not max_saltos) or salto <= max_saltos:
			webs_de_salto = webs_mesmo_dominio[:]
			if not webs_de_salto:
				break
			if salto > 0:
				print
				print "--- SALTO: "+str(salto)+" ---"
				print "Enlaces: "+str(len(webs_de_salto))
				print
			salto += 1
			#SI O MULTIPROCESO ESTA HABILITADO
			if multiproceso:
				Procesos_procesar_web = []
				for w in webs_de_salto:
					args_enlaces_web[0] = w
					webs_mesmo_dominio_extraidas.append(web_a_extraer)
					del webs_mesmo_dominio[0]
					Procesos_procesar_web.append(Fio_procesar_web(args_enlaces_web))
					Procesos_procesar_web[-1].start()
				for fio in Procesos_procesar_web:
					fio.join()
				for fio in Procesos_procesar_web:
					enlaces = enlaces + fio.enlaces
			else:
				while webs_de_salto:
					web_a_extraer = webs_de_salto[0]
					args_enlaces_web[0] = web_a_extraer
					webs_mesmo_dominio_extraidas.append(web_a_extraer)
					del webs_de_salto[0]
					del webs_mesmo_dominio[0]
					enlaces = enlaces + enlaces_web(*args_enlaces_web)
			
	#SOLO A WEB REQUERIDA
	else:
		enlaces = enlaces_web(*args_enlaces_web)
		
	#ELIMINAR ENLACES DUPLICADOS
	enlaces_unicos = []
	for i in enlaces:
		if i not in enlaces_unicos:
			enlaces_unicos.append(i)
	enlaces = enlaces_unicos
	
	#NUMERO DE ENLACES
	print
	print "+"*20
	print "Numero de enlaces totales: "+str(len(enlaces))
	print "+"*20
	print
	
	############################
	#TIPO DE SALIDA
	############################
	#TERMINAL
	if tipo_salida in ["0","terminal","consola"]:
		total = len(enlaces)
		d_total = len(str(total))
		for l in enlaces:
			ceros = d_total-len(str(total))
			string_salida = "0"*ceros+str(total)+" - "+l[0]+"\t"+l[1]
			try:
				string_salida = string_salida.decode("utf8")
			except:
				pass
			print string_salida
			total -= 1
			
	#WEB
	elif tipo_salida in ["1","web","html"]:
		crear_web_datos(web,enlaces)
		
	#DESCARGA
	elif tipo_salida in ["2","descarga","download"]:
		dir_name = web+"-".join(str(x) for x in args_enlaces_web[1:4])+str(max_saltos)
		dir_name = dir_name.replace("/","").replace(":","").replace("?","").replace("|","")
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		descargar(dir_name,enlaces)
	print
	raw_input("Rematado. Pulsa INTRO")
		
def main():
	leer_argumentos(sys.argv)
		
if __name__ == "__main__":
    main()

