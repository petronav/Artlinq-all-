import sys
from lxml import html
from lxml import etree
import requests
import urllib
import csv
import re
import codecs, cStringIO


reload(sys)  
sys.setdefaultencoding('utf8')

search_url = ""
count = 0
list_Params = []
list_index = 0
num_pages = []

	
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
 

def write_scraped_data( search_url,writer, rowtext, fieldnames, cur_artist):
	response  = requests.get(search_url, timeout=60)
	data = response.text.encode('utf-8')
	parsed_body = html.fromstring(data)
	
	list_art_title = parsed_body.xpath('//div[@class="specs"]/table/tr[2]/td[2]/text()')
	print list_art_title
	list_technique = parsed_body.xpath('//div[@class="specs"]/table/tr[3]/td[2]/text()')
	print list_technique
	list_size = parsed_body.xpath('//div[@class="specs"]/table/tr[4]/td[2]/text()')
	print list_size
	list_price = parsed_body.xpath('//div[@class="left"]/p[@class="price"]/text()')
	print list_price
	list_rental = parsed_body.xpath('//div[@class="rent"]/p/b/text()')
	print list_rental
	list_availability = parsed_body.xpath('//div[@class="stock"]/p/span/text()')
	print list_availability
	try:
		rowtext['kunstenaar'] = cur_artist.strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:
		rowtext['titel'] = list_art_title[0].strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:
		rowtext['technique'] = list_technique[0].strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:
		rowtext['size'] = list_size[0].strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:		
		rowtext['price'] = list_price[0].strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:		
		rowtext['rental fee'] = list_rental[0].strip('\r\n\t').encode('utf-8')
		rowtext['rental fee'] = rowtext['rental fee'].replace("Totaal per maand (3%):","")
	except:
		pass
	try:		
		rowtext['availability'] = list_availability[0].strip('\r\n\t').encode('utf-8')
	except:
		pass
	print rowtext
	rowtext['gallery'] = "IQ"
	writer.writerow(rowtext)
   
rowtext = {'gallery': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with codecs.open('artlinq_iq.csv', 'wb', 'utf-8') as csvfile:
	fieldnames = ['gallery', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print fieldname
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	#unicodeW = UnicodeDictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	
	search_url =  "http://www.iq.nl/nl/collectie/onze_collectie/"
	print search_url
	try :
		response  = requests.get(search_url, timeout=60)
		data = response.text.encode('utf-8')
		parsed_body = html.fromstring(data)
		list_art_url = parsed_body.xpath('//div[@class="category"]/a/@href')
		list_artist = parsed_body.xpath('//div[@class="category"]/strong/a/text()')
		
		print list_art_url
		print list_artist
		cur_index = 0
		num_arts = len(list_art_url)
		art_url = search_url.split('/')
		print num_arts
		for arturl in list_art_url:
			cur_art_url = art_url[0] + "//" + art_url[2] + "/" + arturl
			cur_artist = list_artist[cur_index]
			print "artist", cur_artist
			cur_index = cur_index + 1
			print cur_art_url
			artwork_response  = requests.get(cur_art_url, timeout=60)
			artwork_data = artwork_response.text.encode('utf-8')
			#print artwork_data
			artwork_parsed_body = html.fromstring(artwork_data)
			list_artwork_url = artwork_parsed_body.xpath('//div[@class="product"]/a/@href')
			for art in list_artwork_url:
				curarturl = art_url[0] + "//" + art_url[2] + "/" + art
				write_scraped_data( curarturl,writer, rowtext, fieldnames, cur_artist)
			
			
		csvfile.close()
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]