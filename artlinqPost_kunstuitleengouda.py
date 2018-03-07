import sys
from lxml import html
from lxml import etree
import requests
import urllib
import csv
import re
from httplib2 import Http
from urllib import urlencode
from mechanize import Browser

search_url = ""
count = 0
list_Params = []
list_index = 0
num_pages = []

payload = {'grootte': 'Alle Grootten', 'kunstenaar': 'Alle Kunstenaars', 'mode': 'Database', 'orientatie': 'Alle Orientaties', 'status': 'Alle Statussen', 'tariefgroep': 'Alle Tariefgroepen', 'techniek': 'Alle Technieken', 'search': ''} 
  
rowtext = {'kunstuitleen': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with open('artlinq_kunstuitleengouda.csv', 'wb') as csvfile:
	fieldnames = ['kunstuitleen', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	search_url =  "http://www.kunstuitleengouda.nl/zoeken.php"
	search_url =  "http://www.kunstuitleengouda.nl/zoekres.php"
	print search_url
	response  = requests.post(search_url, payload, timeout=60)
	data = response.text.encode('utf-8')
	#print data
	parsed_body = html.fromstring(data)
	list_num_arts = parsed_body.xpath('//body/text()')
	num_results = list_num_arts[0].split(' ')[0]
	print num_results
	
	
	
	for i in range(2,int(num_results)):
		list_arts_title = parsed_body.xpath('//table/tr[' + str(i) + ']/td[3]/text()')
		print list_arts_title
		list_artist = parsed_body.xpath('//table/tr[' + str(i) + ']/td[2]/text()')
		print list_artist
		list_technique = parsed_body.xpath('//table/tr[' + str(i) + ']/td[5]/text()')
		print list_technique
		list_size = parsed_body.xpath('//table/tr[' + str(i) + ']/td[6]/text()')
		print list_size
		list_price = parsed_body.xpath('//table/tr[' + str(i) + ']/td[4]/text()')
		print list_price
		list_availability = parsed_body.xpath('//table/tr[' + str(i) + ']/td[8]/text()')
		print list_availability
		num_arts = len(list_arts_title)
		print num_arts
		try:
			rowtext['titel'] = list_arts_title[0].strip('\t\r\n').encode('utf-8')
		except:
			pass
		try:
			rowtext['kunstenaar'] = list_artist[0].strip('\t\r\n').encode('utf-8')
		except:
			pass
		try:
			rowtext['technique'] = list_technique[0].strip('\t\r\n').encode('utf-8')
		except:
			pass
		try:
			rowtext['size'] = list_size[0].strip('\t\r\n').encode('utf-8')
		except:
			pass
		try:
			rowtext['rental fee'] = list_price[0].strip('\t\r\n').encode('utf-8')
		except:
			pass
		try:
			rowtext['availability'] = list_availability[0].strip('\t\r\n').encode('utf-8')
		except:
			pass
		print rowtext
		rowtext['kunstuitleen'] = "KUNSTUITLEEN GOUDA"
		writer.writerow(rowtext)