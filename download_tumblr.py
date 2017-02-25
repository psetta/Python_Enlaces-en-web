# -*- coding: utf-8 -*-

import os
import sys
import re
import urllib2
import random
from bs4 import BeautifulSoup

def operative_system():
	if os.name == "nt":
		return "windows"
	elif os.name == "poxis":
		return "linux"
	else:
		return None

def into_url():
	if len(sys.argv) > 1:
		url = sys.argv[1]
		if not re.findall("tumblr.com",url):
			print "Insert a Tumblr URL"
			return None
		if not re.findall("^http://",url):
			url = "http://"+url
		return url
	else:
		print "Insert a Tumblr URL"
		return None
	
def read_url(url):
	try:
		print "::URL: "+url
		url_open = urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		print "Error code - %s." % e.code
		return None
	if re.findall("text/html",url_open.info()["content-type"]):
		return url_open.read()
	else:
		return None
		
def clear():
	if operative_system() == "windows":
		os.system("cls")
	elif operative_system() == "linux":
		os.system("clear")
		
def download(archive,dir):
	archive_open_url = urllib2.urlopen(archive)
	#INFO ARCHIVE
	archive_info = archive_open_url.info()
	extension = ""
	if re.findall("video",archive_info["Content-Type"]):
		extension = "."+re.findall("video/(.+)",archive_info["Content-Type"])[0]
	#FILE NAME
	name_file = archive.replace(":","").replace("?","").replace("|","")
	name_file = "".join(name_file.split("/")[-1:])
	dir_and_file_name = dir+"/"+name_file+extension
	file_number = 2
	if os.path.isfile(dir_and_file_name):
		name_file0 = name_file.split(".")[0:-1]
		extension_file = name_file.split(".")[-1]
		if name_file0 and extension_file:
			total_name = dir+"/"+name_file0+"_"+str(file_number)+"."+extension_file
		elif extension:
			total_name = dir+"/"+name_file+"_"+str(file_number)+"."+extension
		while os.path.isfile(total_name):
			file_number += 1
		dir_and_file_name = total_name
	file_dw = file(dir_and_file_name,"wb")
	#ARCHIVE SIZE
	size_bytes = float(archive_info["Content-Length"])
	size_mg = size_bytes / (1024*1024)
	if len(str(size_mg).split(".")) > 1:
		size_mg_show = str(size_mg).split(".")[0]+"."+str(size_mg).split(".")[1][:3]
	else:
		size_mg_show = str(size_mg)
	#BUFFER
	bytes_pp = int(size_bytes / 40)
	bytes_pp = min(bytes_pp, 100000)
	bytes_pp = max(bytes_pp, 30000)
	per = 0
	download_bytes = 0
	while True:
		#CLEAR
		clear()
		#PRINT
		if all_pages:
			print "::URL: "+page_url
		else:
			print "::URL: "+url
		print "::TOTAL: "+str(number_archives)+"/"+str(number_archives_total)
		print "Archive: "+archive
		print "Content-Type: "+archive_info["Content-Type"]
		print "Content-Length: "+size_mg_show+" MiB"
		print "Download... "+str(per)[0:4]+"%"
		#BUFFER
		buffer = archive_open_url.read(bytes_pp)
		if not buffer:
			break
		download_bytes += len(buffer)
		try:
			file_dw.write(buffer)
		except:
			break
		per = (download_bytes/size_bytes)*100
		
def download_archives(archives):
	global number_archives
	global number_archives_total
	if len(archives) > 0:
		dir_name = "_".join(url.split("/")[2:])
		#DIR NAME
		if all_pages:
			dir_name = dir_all_pages
		else:
			dir_number = 2
			if os.path.isdir(dir_name):
				while os.path.isdir(dir_name+"_"+str(dir_number)):
					dir_number += 1
				dir_name = dir_name+"_"+str(dir_number)
			os.mkdir(dir_name)
		#DOWNLAOD ARCHIVES
		number_archives_total = len(archives)
		number_archives = 1
		for archive in archives:
			try:
				download(archive,dir_name)
			except:
				None
			number_archives += 1
	else:
		print "\t- No archives"
		
def extract_archives_url_to_html(html):
	global number_archives_total
	global number_archives
	if html:
		#SOUP
		web_soup = BeautifulSoup(html, "html.parser")
		all_img = []
		all_iframe = []
		#ARTICLE
		all_articles = web_soup.find_all("article")
		for article in all_articles:
			#FIGURE
			try:
				find_figure = article.figure
				if find_figure:
					#IMG
					try:
						if find_figure.find_all("img"):
							find_imgs = find_figure.find_all("img")
							for img in find_imgs:
								all_img.append(img)
					except:
						None
					#IFRAME
					try:
						if find_figure.iframe:
							all_iframe.append(find_figure.iframe)
					except:
						None
			except:
				None
		#LI CLASS=POST
		all_li_post = web_soup.find_all("li", class_="post")
		for post in all_li_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=POSTS
		all_div_posts = web_soup.find_all("div", class_="posts")
		for post in all_div_posts:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=POST
		all_div_post = web_soup.find_all("div", class_="post")
		for post in all_div_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV ID=POSTS
		all_div_post = web_soup.find_all("div", id="posts")
		for post in all_div_post:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#DIV CLASS=ENTRY
		all_div_entry = web_soup.find_all("div", class_="entry")
		for post in all_div_entry:
			#IMG
			try:
				if post.find_all("img"):
					find_imgs = post.find_all("img")
					for img in find_imgs:
						all_img.append(img)
			except:
				None
			#IFRAME
			try:
				if post.iframe:
					all_iframe.append(post.iframe)
			except:
				None
		#EXTRACCION SRC FROM IMG AND IFRAMES
		imgs_src = []
		iframes_src = []
		#SRC IN IMG
		for img in all_img:
			if img["src"]:
				imgs_src.append(img["src"])
		#SRC IN IFRAME
		for iframe in all_iframe:
			if iframe["src"]:
				iframes_src.append(iframe["src"])
		#ARCHIVES
		archives = []
			#IMGS
		for src in imgs_src:
			archives.append(src)
			#IFRAMES
		for src in iframes_src:
			try:
				open_archive_url = urllib2.urlopen(src)
			except:
				open_archive_url = False
			if open_archive_url:
				archive_type = open_archive_url.info()["content-type"]
				if re.findall("text/html",archive_type):
					archive_html = open_archive_url.read()
					#SOUP
					archive_soup = BeautifulSoup(archive_html, "html.parser")
					#SOURCE
					sources = archive_soup.find_all("source")
					for source in sources:
						try:
							archives.append(source["src"])
						except:
							None
					#IMG
					imgs = archive_soup.find_all("img")
					for img in imgs:
						try:
							archives.append(img["src"])
						except:
							None
					#EXTRACT HREF FOR A_LINKS
					#a_tags = archive_soup.find_all("a")
					#for a in a_tags:
					#	try:
					#		archives.append(a["href"])
					#	except:
					#		None
		return list(set(archives))
		
def downlaod_archives_to_page(url):
	html = read_url(url)
	archives = extract_archives_url_to_html(html)
	download_archives(archives)
	
def download_all_pages(url):
	global dir_all_pages
	global page_url
	page = 1
	#DOWNLOAD LOOP
	#CREATE DIR
	dir_number = 2
	dir_all_pages ="_".join(url.split("/")[2:])
	if os.path.isdir(dir_all_pages):
		while os.path.isdir(dir_all_pages+"_"+str(dir_number)):
			dir_number += 1
		dir_all_pages = dir_all_pages+"_"+str(dir_number)
	os.mkdir(dir_all_pages)
	#LOOP
	while True:
		if re.findall("page/$",url):
			complete_url = url+str(page)
		elif re.findall("page$",url):
			complete_url = url+"/"+str(page)
		elif re.findall("/$",url):
			complete_url = url+"page/"+str(page)
		else:
			complete_url = url+"/page/"+str(page)
		page_url = complete_url
		html = read_url(page_url)
		archives = extract_archives_url_to_html(html)
		if len(archives) > 0:
			download_archives(archives)
			page += 1
			clear()
		else:
			#NEXT_PAGE?
			next = False
			soap_html = BeautifulSoup(html, "html.parser")
			all_a_next = soap_html.find_all("a", class_="next")
			if not all_a_next:
				break
			else:
				clear()
				page += 1

###### MAIN
def main(main_url=False,main_all_pages=False):
	clear()
	global url
	global all_pages
	#URL
	if main_url:
		url = main_url
	else:
		url = into_url()
	#ALL_PAGES
	if main_all_pages:
		all_pages = main_all_pages
	else:
		if len(sys.argv) > 2:
			all_pages = True if sys.argv[2] in ["1","True"] else False
		else:
			all_pages = False
	#LAUNCH
	if url:
		if all_pages:
			download_all_pages(url)
		else:
			downlaod_archives_to_page(url)

if __name__ == "__main__":			
	main()
	
	