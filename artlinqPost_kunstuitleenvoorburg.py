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

payload = {'PrijsCat': '(Geen selectie)', 'Techniek': '(Geen selectie)'} 


def write_scraped_data( search_url,writer, rowtext, fieldnames ):
	response  = requests.get(search_url, timeout=30)
	data = response.text.encode('utf-8')
	parsed_body = html.fromstring(data)
	#list_arts = parsed_body.xpath('//div[@class="nietcompact"]')
	print list_Params[list_index]['xpath1']
	list_arts = parsed_body.xpath(list_Params[list_index]['xpath1'])
	print "num arts", len(list_arts)
	for cur_art in list_arts:
		count = 0
		rental_index = 0
		cur_array = cur_art.getchildren()
		for child in cur_art:
			print count, child.tag
			if child.tag == 'a':
				#if count == 0 or count == 1:
					child_items_array = child.items()
					print len(child_items_array)
					for child_item in child_items_array:
						print child_item
						#print child.getchildren()
						#print child.getchildren()[0].getchildren()[0]
						#print child.getchildren()[0].getchildren()[0].getchildren()
						#print etree.tostring(child.getchildren()[0], pretty_print=True)
						if child_item[0] == 'title' or child_item[0] == 'caption':
							cur_item_count = 0
							data_array = child_item[1].split('|')
							for d in data_array:
								if cur_item_count == int(list_Params[list_index]['titel']):
									print "titel"
									rowtext[fieldnames[2]] = d.encode('utf-8').strip('\n')
									print rowtext[fieldnames[2]], fieldnames[2]
								elif cur_item_count == int(list_Params[list_index]['size']):
									print "size"
									rowtext[fieldnames[5]] = d.encode('utf-8').strip('\n')
									print rowtext[fieldnames[5]], fieldnames[5]
								elif cur_item_count == int(list_Params[list_index]['kunstenaar']):
									print "artist"
									rowtext[fieldnames[1]] = d.encode('utf-8').strip('\n')
									print rowtext[fieldnames[1]], fieldnames[1]
								elif cur_item_count == int(list_Params[list_index]['technique']):
									print "technique"
									rowtext[fieldnames[3]] = d.encode('utf-8').strip('\n')
									print rowtext[fieldnames[3]], fieldnames[3]
								elif cur_item_count == int(list_Params[list_index]['availability']):
									print "availability"
									rowtext[fieldnames[10]] = d.encode('utf-8').strip('\n')
									print rowtext[fieldnames[10]], fieldnames[10]
								elif cur_item_count == int(list_Params[list_index]['price']):
									print "price"
									rowtext[fieldnames[8]] = d.encode('utf-8').strip('\n')
									print rowtext[fieldnames[8]], fieldnames[8]
								elif cur_item_count == int(list_Params[list_index]['rental']):
									print "rental"
									rowtext[fieldnames[9]] = d.encode('utf-8').strip('\n')
									print rowtext[fieldnames[9]], fieldnames[9]
								cur_item_count = cur_item_count + 1
			else:
				temp_text = etree.tostring(child, pretty_print=True)
				#print "Child: ", temp_text
				if count < 10:
					temp_text = temp_text.split('>', 1)[1]
					#print temp_text
					temp_text = temp_text.rsplit('<', 1)[0]
					#print temp_text
					temp_text = temp_text.rstrip('\n')
					#print temp_text
				if rental_index > 0 and count == rental_index + 1 and 'div' not in temp_text:
					rowtext[fieldnames[10]] = temp_text.strip('\n')
					print count, temp_text,fieldnames[10], rowtext[fieldnames[10]]
				if count >= (int(list_Params[list_index]['rental']) - 1) and count < (int(list_Params[list_index]['rental']) + 1):
					print "rental", temp_text
					if 'per mnd' in temp_text or 'p/m' in temp_text:
						rowtext[fieldnames[9]] = temp_text.strip('\n')
						rental_index = count
						print count, temp_text,fieldnames[9], rowtext[fieldnames[9]]
						print rowtext
				if count == (int(list_Params[list_index]['gallery']) - 1) or count == int(list_Params[list_index]['gallery']):
					print "gallery"
					if not temp_text == rowtext[fieldnames[10]]:
						rowtext[fieldnames[0]] = temp_text.strip('\n')
						print count, temp_text, fieldnames[0]
						print rowtext
				if count == int(list_Params[list_index]['kunstenaar']):
					print "artist"
					rowtext[fieldnames[1]] = temp_text.strip('\n')
					print count, temp_text, fieldnames[1]
					print rowtext
				if count == int(list_Params[list_index]['titel']):
					print "titel"
					rowtext[fieldnames[2]] = temp_text.strip('\n')
					print count, temp_text, fieldnames[2]
					print rowtext
				if count == int(list_Params[list_index]['size']):
					print "size"
					if len(temp_text.split(',')) > 1:
						rowtext[fieldnames[5]] = temp_text.split(',')[1]
						print count, temp_text, fieldnames[5]
						print rowtext
					else:
						rowtext[fieldnames[5]] = temp_text
						print count, temp_text, fieldnames[5]
						print rowtext
						
				if count == int(list_Params[list_index]['technique']):
					print "technique"
					if len(temp_text.split(',')) > 1:
						rowtext[fieldnames[3]] = temp_text.split(',')[0]
						#rowtext[fieldnames[3]] = temp_text.strip('\n')
						print count, temp_text, fieldnames[3]
						print rowtext
					else:
						rowtext[fieldnames[3]] = temp_text
						#rowtext[fieldnames[3]] = temp_text.strip('\n')
						print count, temp_text, fieldnames[3]
						print rowtext

				if count == int(list_Params[list_index]['availability']) and 'div' not in temp_text:
					print "availability"
					#if len(temp_text) < 40 :
					rowtext[fieldnames[10]] = temp_text.strip('\n')
					print count, temp_text, fieldnames[10]
					print rowtext
				if count == int(list_Params[list_index]['price']):
					print "price"
					rowtext[fieldnames[8]] = temp_text.strip('\n')
					print count, temp_text, fieldnames[8]
					print rowtext

				#sys.stdin.read(1)
			count = count + 1
		#print rowtext
		#sys.stdin.read(1)
		if int(list_Params[list_index]['kunstenaar']) == 100:
			list_artist = parsed_body.xpath(list_Params[list_index]['kunstenaarxpath'])
			if len(list_artist)>0:
				rowtext[fieldnames[1]] = list_artist[0].encode('utf-8').strip('\n')
		if int(list_Params[list_index]['availability']) == 100:
			list_availability = parsed_body.xpath(list_Params[list_index]['availabilityxpath'])
			if len(list_availability)>0:
				rowtext[fieldnames[10]] = list_availability[0].encode('utf-8').strip('\n')		
		if int(list_Params[list_index]['technique']) == 100:
			list_technique = parsed_body.xpath(list_Params[list_index]['techniquexpath'])
			if len(list_technique)>0:
				rowtext[fieldnames[10]] = list_technique[0].encode('utf-8').strip('\n')		
		writer.writerow(rowtext)
   
rowtext = {'kunstuitleen': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with open('artlinq_kunstuitleenvoorburg.csv', 'wb') as csvfile:
	fieldnames = ['kunstuitleen', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	search_url =  "http://www.kunstuitleenvoorburg.nl/collectie/resultaat.asp"
	print search_url
	response  = requests.post(search_url, payload, timeout=60)
	data = response.text.encode('utf-8')
	#print data
	parsed_body = html.fromstring(data)
	list_num_arts = parsed_body.xpath('//body/h1/text()')
	num_arts = list_num_arts[0]
	print num_arts
	list_page_num = parsed_body.xpath('//div[@class="pag"]/text()')
	num_pages = list_page_num[0].split(' ')[4]
	print num_pages
	page_tag = "?pag="
	#list_arts_title = parsed_body.xpath('//div[@class="art_item"]/div[@class="art-description"]/h3/text()')
	list_arts_title = parsed_body.xpath('//div[@class="art-description"]/h3/text()')
	print list_arts_title
	list_artist = parsed_body.xpath('//div[@class="art-description"]/p[@class="artist"]/a/text()')
	print list_artist
	list_size = parsed_body.xpath('//div[@class="art-description"]/ul/li[1]/text()')
	print list_size
	list_price = parsed_body.xpath('//div[@class="art-description"]/ul/li[3]/text()')
	print list_price
	list_availability = parsed_body.xpath('//div[@class="art-description"]/p[2]/span/text()')
	print list_availability
	num_arts = len(list_arts_title)
	for i in range(0,num_arts):
		rowtext['titel'] = list_arts_title[i].strip('\t\r\n').encode('utf-8')
		rowtext['kunstenaar'] = list_artist[i].strip('\t\r\n').encode('utf-8')
		rowtext['size'] = list_size[i].strip('\t\r\n').encode('utf-8')
		rowtext['price'] = list_price[i].strip('\t\r\n').encode('utf-8')
		rowtext['availability'] = list_availability[i].strip('\t\r\n').encode('utf-8')
		print rowtext
		writer.writerow(rowtext)
	for page_num in range(2,int(num_pages)+1):
		current_search_url = search_url + page_tag + str(page_num)
		print current_search_url
		response  = requests.post(current_search_url, payload, timeout=60)
		data = response.text.encode('utf-8')
		print data
		parsed_body = html.fromstring(data)
		#list_num_arts = parsed_body.xpath('//body/h1/text()')
		#print list_num_arts
		#num_arts = list_num_arts[0]
		#list_page_num = parsed_body.xpath('//div[@class="pag"]/text()')
		#num_pages = list_page_num[0].split(' ')[4]
		#page_tag = "pag="
		list_arts_title = parsed_body.xpath('//div[@class="art-description"]/h3/text()')
		print len(list_arts_title)
		list_artist = parsed_body.xpath('//div[@class="art-description"]/p[@class="artist"]/a/text()')
		list_size = parsed_body.xpath('//div[@class="art-description"]/ul/li[1]/text()')
		list_price = parsed_body.xpath('//div[@class="art-description"]/ul/li[3]/text()')
		list_availability = parsed_body.xpath('//div[@class="art-description"]/p[2]/span/text()')
		num_arts = len(list_arts_title)
		for i in range(0,num_arts):
			rowtext['titel'] = list_arts_title[i].strip('\t\r\n').encode('utf-8')
			rowtext['kunstenaar'] = list_artist[i].strip('\t\r\n').encode('utf-8')
			rowtext['size'] = list_size[i].strip('\t\r\n').encode('utf-8')
			rowtext['price'] = list_price[i].strip('\t\r\n').encode('utf-8')
			rowtext['availability'] = list_availability[i].strip('\t\r\n').encode('utf-8')
			print rowtext
			writer.writerow(rowtext)
		
		
	