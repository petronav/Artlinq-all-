import sys
from lxml import html
from lxml import etree
import requests
import urllib
import csv

search_url = ""
count = 0

def write_scraped_data( search_url,writer, rowtext, fieldnames ):
	print "url", search_url
	response  = requests.get(search_url, timeout=30)
	print "status", response.status_code
	data = response.text.encode('utf-8')
	parsed_body = html.fromstring(data)
	list_arts = parsed_body.xpath('//div[@class="nietcompact3"]')
	print "num arts",len(list_arts)
	for cur_art in list_arts:
		count = 0
		rental_index = 0
		cur_array = cur_art.getchildren()
		for child in cur_art:
			print count, child.tag
			if child.tag == 'a':
				if count == 0:
					child_items_array = child.items()
					print len(child_items_array)
					for child_item in child_items_array:
						print child_item
						if child_item[0] == 'title':
							cur_item_count = 0
							data_array = child_item[1].split('|')
							for d in data_array:
								if cur_item_count == 1:
									print "title"
									rowtext[fieldnames[2]] = d.encode('utf-8')
									print rowtext[fieldnames[2]], fieldnames[2]
								elif cur_item_count == 3:
									print "size"
									rowtext[fieldnames[5]] = d.encode('utf-8')
									print rowtext[fieldnames[5]], fieldnames[5]
								elif cur_item_count == 0:
									print "artist"
									rowtext[fieldnames[1]] = d.encode('utf-8')
									print rowtext[fieldnames[1]], fieldnames[1]
								elif cur_item_count == 2:
									print "technique"
									rowtext[fieldnames[3]] = d.encode('utf-8')
									print rowtext[fieldnames[3]], fieldnames[3]
								elif cur_item_count == 4:
									print "availability"
									rowtext[fieldnames[10]] = d.encode('utf-8')
									print rowtext[fieldnames[10]], fieldnames[10]
								elif cur_item_count == 5:
									print "price"
									d = d.split(':')[1]
									rowtext[fieldnames[8]] = d.strip(' ').encode('utf-8')
									print rowtext[fieldnames[8]], fieldnames[8]
								elif cur_item_count == 6:
									print "rental"
									rowtext[fieldnames[9]] = d.encode('utf-8')
									print rowtext[fieldnames[9]], fieldnames[9]
								cur_item_count = cur_item_count + 1
			count = count + 1
		#print rowtext
		#sys.stdin.read(1)
		rowtext["gallery"]="kunstonline"
		writer.writerow(rowtext)
   
rowtext = {'gallery': '', 'kunstenaar': '', 'title':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with open('artlinq.csv', 'w') as csvfile:
	fieldnames = ['gallery', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print fieldname
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	search_url =  urllib.unquote(urllib.unquote(sys.argv[1]))
	try :
		#response  = requests.get(search_url, timeout=30)
		#data = response.text.encode('utf-8')
		#parsed_body = html.fromstring(data)
		#list_iframe = parsed_body.xpath('//a[@class="openframe fancybox.iframe"]/@href')
		#search_url = search_url.rsplit('/', 1)[0]
		#search_url = search_url + "/" + list_iframe[0]
		page = 0
		write_scraped_data(search_url,writer, rowtext, fieldnames)
		search_url = search_url.rsplit('?', 1)[0]
		search_supp = "&Cat=1&Prcat=0&Beschikbaar=0&Compact=0&="
		search_page = "?pag="
		for i in range(2,62	):
			page = i
			search_page = search_page + str(page)
			search_url = search_url + search_page + search_supp
			#print search_url
			#write_scraped_data(search_url,writer, rowtext, fieldnames)
			search_url = search_url.rsplit('?', 1)[0]
			search_page = "?pag="
			
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]