# -*- coding: utf-8 -*-

import sys
import re
import urllib2
import random
import os
import time

urlopen_timeout = 20

def replace_code(url):
	replaced_url = url.replace("%3A",":").replace("%2F","/").replace("%3F","?")
	replaced_url = replaced_url.replace("%3D","=").replace("%26","&").replace("&amp","")
	replaced_url = replaced_url.replace("%252F","//").replace("%252C",",")
	return replaced_url

def descargar(url):
	file_url = urllib2.urlopen(url)
	name_file = url.replace("/","").replace(":","").replace("?","").replace("|","")
	name_file = name_file.split(".flv")[0]+".flv"
	try:
		arquivo = file(name_file,"wb")
	except:
		name_file = str(random.randint(100,10000))+".flv"
		arquivo = file(name_file,"wb")
	video_header = file_url.info()
	tamanho_bytes = float(video_header["Content-Length"])
	tamanho_mg = tamanho_bytes / (1024*1024)
	bytes_descargados = 0
	bytes_pp = int(tamanho_bytes / 40)
	bytes_pp = min(bytes_pp, 100000)
	bytes_pp = max(bytes_pp, 5000)
	porcentaje = 0
	while True:
		os.system("cls")
		print "> "+url
		print "Content-Type: "+video_header["Content-Type"]
		print "Content-Length: "+str(tamanho_mg)+" MiB"
		print "Descargando: "+str(porcentaje)+"%"
		buffer = file_url.read(bytes_pp)
		if not buffer:
			break
		bytes_descargados += len(buffer)
		arquivo.write(buffer)
		porcentaje = (bytes_descargados/tamanho_bytes)*100
		
	#video_code = file_url.read()
	#arquivo.write(video_code)
	arquivo.close()
	print "Descarga finalizada"
	
def descargar_flvurl(url):
	url_info = urllib2.urlopen(url, timeout=urlopen_timeout)
	#header_web = url_info.info()
	#print "::URL: "+url
	#print header_web
	web_code = url_info.read()
	web_code = web_code.replace("'",'"')
	flv_enlaces_pre = re.findall("flv_?url=([^;]+)",web_code)
	flv_enlaces = [replace_code(x) for x in flv_enlaces_pre]
	if len(flv_enlaces) > 0:
		for link in flv_enlaces:
			try:
				descargar(link)
			except:
				#print "ERROR - Imposible descargar "+link
				None

if __name__ == "__main__":
	if len(sys.argv) > 1:
		descargar_flvurl(sys.argv[1])
	else:
		print("Introducir url como argumento")
