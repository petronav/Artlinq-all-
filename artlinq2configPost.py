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

payload = {'bSubmitted': '1', 'tab': 'adv', 'iresultsperpage': '48', 'idKleuren': '-1', 'idStijlen': '-1', 'idFormatenBreedte': '-1', 'idFormatenHoogte': '-1', 'idOnderwerpen': '-1', 'idPrijzen': '-1', 'afb_titel': '', 'b3donly': '1', 'bbeschikbaar':'1','Zoeken': 'SUBMIT'} 

with open('artlinq_config.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		print(row['url'], row['iframe'], row['xpath1'], row['kunstenaar'], row['titel'], row['technique'], row['size'], row['availability'], row['price'], row['rental'], row['gallery'], row['numpages'], row['pagetag'], row['pagesupptag'],row['kunstenaarxpath'],row['availabilityxpath'],row['techniquexpath'])
		list_Params.append(row)
		num_pages.append(row['numpages'])

for param in list_Params:
	print "URL:", param['url']
	print "URL:", param['iframe']
	print "xpath1", param['xpath1']
	print "kunstenaar:", param['kunstenaar']
	print "titel", param['titel']
	print "technique:", param['technique']
	print "size", param['size']
	print "availability:", param['availability']
	print "price", param['price']
	print "rental:", param['rental']
	print "gallery", param['gallery']
	print "numpages", param['numpages']
	print "pagetag", param['pagetag']
	print "pagesupptag", param['pagesupptag']
	print "kunstenaarxpath", param['kunstenaarxpath']
	print "availabilityxpath", param['availabilityxpath']
	print "techniquexpath", param['techniquexpath']
	


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
with open('artlinq.csv', 'wb') as csvfile:
	fieldnames = ['kunstuitleen', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print fieldname
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	list_index = int(sys.argv[1])
	search_url =  urllib.unquote(urllib.unquote(list_Params[list_index]['url']))
	print search_url
	payload = {'bSubmitted': '1', 'tab': 'adv', 'iresultsperpage': '48', 'idKleuren': '-1', 'idStijlen': '-1', 'idFormatenBreedte': '-1', 'idFormatenHoogte': '-1', 'idOnderwerpen': '-1', 'idPrijzen': '-1', 'afb_titel': '', 'b3donly': '1', 'bbeschikbaar':'1','Zoeken': 'SUBMIT'}
	form_count = 0
	try :
		br = Browser()
		br.set_handle_robots(False)
		br.open(search_url)
		for form in br.forms():
			form_count = form_count + 1
			print "Form name:", form.name
			#print form
			if form_count == 3:
				for control in form.controls:
					if control.name == 'idKleuren' or control.name == 'idStijlen' or control.name == 'idFormatenBreedte' or control.name == 'idFormatenHoogte' or control.name == 'idOnderwerpen' or control.name == 'idPrijzen'or control.name == 'idTechnieken' :
						control.value = ['-1',]
					elif control.name == 'afb_titel':
						control.value = ''
					elif control.name == 'b3donly' or control.name == 'bbeschikbaar':
						control.value = ['1',]
					elif control.name == 'bSubmitted' or control.name == 'tab' or control.name == 'iresultsperpage':
						pass
					else:
						control.readonly = False
						control.value = 'submit'
						control.click()
					#print control
				#br.select_form("search_form")
				#form['bSubmitted'] = '1'
				#form['tab'] = 'adv'
				#form['iresultsperpage'] = '48'
				form['idKleuren'] = ['-1',]
				print "set idKleuren"
				form['idStijlen'] = ['-1',]
				print "set idStijlen"
				form['idFormatenBreedte'] = ['-1',]
				print "set idFormatenBreedte"
				form['idFormatenHoogte'] = ['-1',]
				print "set idFormatenHoogte"
				form['idOnderwerpen'] = ['-1',]
				print "set idOnderwerpen"
				form['idPrijzen'] = ['-1',]
				print "set idPrijzen"
				form['afb_titel'] = ''
				print "set afb_titel"
				form['b3donly'] = ['1',]
				print "set b3donly"
				form['bbeschikbaar'] = ['1',]
				print "set bbeschikbaar"
				pag2 = br.submit()
				html = pag2.read()
				print html
				#h = Http()
		#response, content = h.request(search_url, "POST", urlencode(payload))
		#response  = requests.post(search_url, params=payload, timeout=30)
		#print response
		#print content
		#print response.status_code
		#data = response.text.encode('utf-8')
		#print data
		# parsed_body = html.fromstring(data)
		# if list_Params[list_index]['iframe']:
			# list_iframe = parsed_body.xpath(list_Params[list_index]['iframe'])
			# if "http" not in list_iframe[0]:
				# search_url = search_url.rsplit('/', 1)[0]
				# search_url = search_url + "/" + list_iframe[0]
			# else:
				# search_url = list_iframe[0] + "/catalogus.asp?cat=1&compact=0"
		# print "search url",search_url
		# print "history",response.history
		# print search_url
		# response  = requests.post(search_url, params=payload, timeout=30)
		# #print "response code", response.status_code
		# print response.url
		# print response.status_code
		# data = response.text.encode('utf-8')
		# #print data
		# parsed_body = html.fromstring(data)
		# list_script = parsed_body.xpath("//script/text()")
		# #tag = etree.toString(list_script[0], pretty_print=True)
		# temp = list_script[0].strip('\r\n')
		# temp = re.search('location="(.+?)";', temp)
		# if temp:
			# search_url = search_url + temp.group(1)
		# print "search url",search_url
		# page = 0
		# #write_scraped_data(search_url,writer, rowtext, fieldnames)
		# search_url = search_url.rsplit('?', 1)[0]
		# #search_supp = "&Cat=1&Prcat=0&Beschikbaar=0&Compact=0&="
		# search_supp = list_Params[list_index]['pagesupptag']
		# #search_page = "?pag="
		# search_page = list_Params[list_index]['pagetag']
		
		# for i in range(2,int(num_pages[list_index]) + 1):
			# page = i
			# #list_index = list_index + 1
			# search_page = search_page + str(page)
			# current_search_url = search_url + search_page + search_supp
			# print current_search_url
			# #write_scraped_data(current_search_url,writer, rowtext, fieldnames)
			# search_url = current_search_url.rsplit('?', 1)[0]
			# search_page = list_Params[list_index]['pagetag']
			# search_supp = list_Params[list_index]['pagesupptag']
			
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]