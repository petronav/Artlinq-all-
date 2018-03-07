import sys
from lxml import html
from lxml import etree
import requests
import urllib
import csv
import re
import codecs, cStringIO
from mechanize import Browser
import json

search_url = ""
count = 0


reload(sys)  
sys.setdefaultencoding('utf8')
	
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
 
    def __iter__(self):
        return self
 
    def next(self):
        return self.reader.next().encode("utf-8")
 
class UnicodeDictReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
 
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
        self.header = self.reader.next()
 
    def next(self):
        row = self.reader.next()
        vals = [unicode(s, "utf-8") for s in row]
        return dict((self.header[x], vals[x]) for x in range(len(self.header)))
 
    def __iter__(self):
        return self
 
class UnicodeDictWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
 
    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.fieldnames = fieldnames
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
        
    def writeheader(self):
        self.writer.writerow(self.fieldnames)
 
    def writerow(self, row):
        self.writer.writerow([row[x].encode("utf-8") for x in self.fieldnames])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
 
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
 

def write_scraped_data( item, data_url,writer, rowtext, fieldnames ):
	#print item['field_main_image']
	match = re.search(r'href=[\'"]?([^\'" >]+)', item['field_main_image'])
	if match:
		art_url = match.group(0).split('"')[1]
	art_url = data_url + art_url
	art_response  = requests.get(art_url, timeout=30)
	art_data = art_response.text.encode('utf-8')
	art_parsed_body = html.fromstring(art_data)
	list_art_name = art_parsed_body.xpath('//div[@class="the_content"]/h1/text()')
	rowtext['titel'] = list_art_name[0].encode('utf-8')
	

	print rowtext['titel']
	list_artist_name = art_parsed_body.xpath('//div[@class="the_content"]/span[2]/div/div/div/a/text()')
	if len(list_artist_name) == 0:
		list_artist_name = art_parsed_body.xpath('//div[@class="the_content"]/span[1]/div/div/div/a/text()')
		rowtext['kunstenaar'] = list_artist_name[0].encode('utf-8')
		print rowtext['kunstenaar']
		list_technique = art_parsed_body.xpath('//div[@class="the_content"]/span[2]/div/div/div/text()')
		rowtext['technique'] = list_technique[0].encode('utf-8')
		print rowtext['technique']
		list_height = art_parsed_body.xpath('//div[@class="the_content"]/span[5]/div[@class="field field-name-field-height field-type-text field-label-hidden"]/div/div/text()')
		list_width = art_parsed_body.xpath('//div[@class="the_content"]/span[6]/div[@class="field field-name-field-width field-type-text field-label-hidden"]/div/div/text()')
		rowtext['size'] = list_height[0].encode('utf-8') + 'X' + list_width[0].encode('utf-8')
		print rowtext['size']
		list_depth = art_parsed_body.xpath('//div[@class="the_content"]/span[8]/text()')
		print list_depth
		if u"Prijs :" not in list_depth[0] or u"Huurprijs" not in list_depth[0]:
			temp_text = etree.tostring(list_depth[0].encode('utf-8'), pretty_print=True)
			print temp_text
		if rowtext['titel'] == 'Insect' or rowtext['titel'] == 'Hide Away Cozy Adult' or rowtext['titel'] == 'Speaker' or rowtext['titel'] == 'Hours of dark, twee-luik':
			list_price = art_parsed_body.xpath('//div[@class="the_content"]/span[8]/text()')
			rowtext['price'] = list_price[0].encode('utf-8')
			print rowtext['price']
			list_rental = art_parsed_body.xpath('//div[@class="the_content"]/span[9]/text()')
			rowtext['rental fee'] = re.findall(r'\d+', list_rental[0])[0].encode('utf-8')
			print rowtext['rental fee']
		else:
			list_price = art_parsed_body.xpath('//div[@class="the_content"]/span[7]/text()')
			rowtext['price'] = re.findall(r'\d+', list_price[0])[0].encode('utf-8')
			print rowtext['price']
			list_rental = art_parsed_body.xpath('//div[@class="the_content"]/span[8]/text()')
			rowtext['rental fee'] = re.findall(r'\d+', list_rental[0])[0].encode('utf-8')
			print rowtext['rental fee']

	else:
		#print list_artist_name
		rowtext['kunstenaar'] = list_artist_name[0].encode('utf-8')
		print rowtext['kunstenaar']
		list_technique = art_parsed_body.xpath('//div[@class="the_content"]/span[3]/div/div/div/text()')
		rowtext['technique'] = list_technique[0].encode('utf-8')
		print rowtext['technique']
		list_height = art_parsed_body.xpath('//div[@class="the_content"]/span[6]/div[@class="field field-name-field-height field-type-text field-label-hidden"]/div/div/text()')
		list_width = art_parsed_body.xpath('//div[@class="the_content"]/span[7]/div[@class="field field-name-field-width field-type-text field-label-hidden"]/div/div/text()')
		rowtext['size'] = list_height[0].encode('utf-8') + 'X' + list_width[0].encode('utf-8')
		print rowtext['size']
		list_depth = art_parsed_body.xpath('//div[@class="the_content"]/span[8]')
		print list_depth
		if "Prijs :" not in list_depth[0] or "Huurprijs" not in list_depth[0]:
			temp_text = etree.tostring(list_depth[0].encode('utf-8'), pretty_print=True)
			print temp_text
		if rowtext['titel'] == 'Insect' or rowtext['titel'] == 'Hide Away Cozy Adult' or rowtext['titel'] == 'Speaker' or rowtext['titel'] == 'Hours of dark, twee-luik':
			list_price = art_parsed_body.xpath('//div[@class="the_content"]/span[9]/text()')
			rowtext['price'] = re.findall(r'\d+', list_price[0])[0].encode('utf-8')
			print rowtext['price']
			list_rental = art_parsed_body.xpath('//div[@class="the_content"]/span[10]/text()')
			rowtext['rental fee'] = re.findall(r'\d+', list_rental[0])[0].encode('utf-8')
			print rowtext['rental fee']
		else:
			list_price = art_parsed_body.xpath('//div[@class="the_content"]/span[8]/text()')
			rowtext['price'] = re.findall(r'\d+', list_price[0])[0].encode('utf-8')
			print rowtext['price']
			list_rental = art_parsed_body.xpath('//div[@class="the_content"]/span[9]/text()')
			rowtext['rental fee'] = re.findall(r'\d+', list_rental[0])[0].encode('utf-8')
			print rowtext['rental fee']
	print rowtext
	writer.writerow(rowtext)

   
rowtext = {'kunstuitleen': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with codecs.open('artlinq.csv', 'wb', 'utf-8') as csvfile:
	fieldnames = ['kunstuitleen', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print fieldname
	
	writer = UnicodeDictWriter(csvfile, fieldnames=fieldnames)
	#unicodeW = UnicodeDictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	search_url =  "http://www.heden.nl/system/heden/collections/"
	data_url = "http://www.heden.nl"
	search_url_supp = "/fragment?format=All&price=All"
	search_page = 0
	cur_search_url = search_url + str(search_page) + search_url_supp
	print cur_search_url
	try :
		response  = requests.get(cur_search_url, timeout=30)
		data = response.json()
		num_items = len(data['items'])
		print num_items
		for item in data['items']:
			write_scraped_data( item, data_url,writer, rowtext, fieldnames )
		while num_items > 0:
			search_page = search_page + 1
			cur_search_url = search_url + str(search_page) + search_url_supp
			print cur_search_url
			response  = requests.get(cur_search_url, timeout=30)
			data = response.json()
			num_items = len(data['items'])
			print num_items
			for item in data['items']:
				write_scraped_data( item, data_url,writer, rowtext, fieldnames )
		csvfile.close()
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]