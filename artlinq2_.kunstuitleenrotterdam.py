import sys
from lxml import html
from lxml import etree
import requests
import urllib
import csv

reload(sys)  
sys.setdefaultencoding('utf8')

search_url = ""
count = 0

def write_scraped_data( search_url,writer, rowtext, fieldnames ):
	response  = requests.get(search_url, timeout=30)
	data = response.text.encode('utf-8')
	parsed_body = html.fromstring(data)
	list_art_detail = parsed_body.xpath('//div[@class="gridder-list"]/p/text()')
	list_art_rental = parsed_body.xpath('//div[@class="gridder-list"]/p/strong/text()')
	list_art_title = parsed_body.xpath('//div[@class="gridder-list"]/p/i/text()')
	#print list_art_title
	count = 0
	print "list_art"
	print etree.tostring(list_art_detail, pretty_print=True)
	print etree.tostring(list_art_rental, pretty_print=True)
	for art_detail in list_art_detail:
		#print "art: ", art_detail
		art_detail = art_detail.strip('\r\n\t').split('|')
		print art_detail.encode('utf-8')
		print list_art_title[int(count/4)].encode('utf-8')
		print list_art_rental[int(count/4)].encode('utf-8')
		if count == 0 :
			rowtext['kunstenaar'] = art_detail[0].strip('\r\n\t').encode('utf-8')
			rowtext['titel'] = list_art_title[int(count/4)].strip('\r\n\t').encode('utf-8')
		elif count == 2:
			rowtext['technique'] = art_detail[0].strip('\r\n\t').encode('utf-8')
			rowtext['size'] = art_detail[1].strip('\r\n\t').encode('utf-8')
		if count == 3:
			print rowtext
			rowtext['gallery'] = "KUNSTUITLEEN ROTTERDAM"
			writer.writerow(rowtext)
		count = count + 1
   
rowtext = {'gallery':'', 'kunstuitleen': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with open('artlinq_kunstuitleenrotterdam.csv', 'w') as csvfile:
	fieldnames = ['gallery', 'kunstuitleen', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	search_url =  "http://kunstuitleenrotterdam.nu/collectie/uitleencollectie"
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
	}
	print search_url
	try :
		response  = requests.get(search_url, headers=headers, timeout=60)
		data = response.text.encode('utf-8')
		#print data
		parsed_body = html.fromstring(data)
		list_iframe = parsed_body.xpath('//iframe/@src')
		print list_iframe
		search_url = list_iframe[0]
		print search_url
		page = 0
		write_scraped_data(search_url,writer, rowtext, fieldnames)
		search_url = search_url.rsplit('?', 1)[0]
		search_supp = "&Cat=1&Prcat=0&Beschikbaar=0&Compact=0&="
		search_page = "?pag="
		for i in range(2,13	):
			page = i
			search_page = search_page + str(page)
			search_url = search_url + search_page + search_supp
			print search_url
			write_scraped_data(search_url,writer, rowtext, fieldnames)
			search_url = search_url.rsplit('?', 1)[0]
			search_page = "?pag="
			
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]