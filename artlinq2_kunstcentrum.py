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
			
def write_scraped_data( search_url,writer, rowtext, fieldnames ):
	response  = requests.get(search_url, timeout=60)
	print "write data", search_url
	data = response.text.encode('utf-8')
	#print data
	parsed_body = html.fromstring(data)
	#list_arts = parsed_body.xpath('//div[@class="nietcompact"]')
	
	list_art_title = parsed_body.xpath('//div[@class="artwork-detail"]/p[1]/em/text()')
	#print list_art_title
	list_art_size = parsed_body.xpath('//div[@class="artwork-detail"]/p[2]/text()')
	#print list_art_size
	list_art_technique = parsed_body.xpath('//div[@class="artwork-detail"]/p[3]/text()')
	#print list_art_technique
	list_art_price = parsed_body.xpath('//div[@class="artwork-detail"]/p[4]/text()')
	#print list_art_price
	list_art_rental = parsed_body.xpath('//div[@class="artwork-detail"]/p[5]/text()')
	#print list_art_rental
	list_artist = parsed_body.xpath('//div[@class="resultsheading"]/p/a/text()')
	#print list_artist
	num_arts = len(list_art_title)
	for i in range (0, num_arts):
		rowtext['gallery'] = "Kunstcentrum Zaandam"
		list_artist_temp = parsed_body.xpath('//div[@class="resultsheading"][' + str(i) + ']/p/a/text()')
		try:
			rowtext['kunstenaar'] = list_artist_temp[0].strip('\r\n\t').encode('utf-8')
		except:
			pass
		list_art_title_temp = parsed_body.xpath('//div[@class="artwork-detail"][' + str(i) + ']/p[1]/em/text()')
		try:
			rowtext['titel'] = list_art_title_temp[0].strip('\r\n\t').encode('utf-8')
		except:
			pass
		list_art_technique_temp = parsed_body.xpath('//div[@class="artwork-detail"][' + str(i) + ']/p[3]/text()')
		try:
			rowtext['technique'] = list_art_technique_temp[0].strip('\r\n\t').encode('utf-8')
		except:
			pass
		list_art_size_temp = parsed_body.xpath('//div[@class="artwork-detail"][' + str(i) + ']/p[2]/text()')
		#print list_art_size_temp
		try:
			temp = list_art_size_temp[0].replace("hxb:","")
			temp = temp.replace("hxbxd:","")
			temp = temp.rstrip(' ')
			temp = temp.lstrip(' ')
			rowtext['size'] = temp.encode('utf-8')
		except:
			pass
		list_art_price_temp = parsed_body.xpath('//div[@class="artwork-detail"][' + str(i) + ']/p[4]/text()')
		try:
			temp = list_art_price_temp[0].replace("verkoopprijs:","")
			temp = temp.rstrip(' ')
			temp = temp.lstrip(' ')
			rowtext['price'] = temp.strip('\r\n\t').encode('utf-8')
		except:
			pass
		list_art_rental_temp = parsed_body.xpath('//div[@class="artwork-detail"][' + str(i) + ']/p[5]/text()')
		try:
			temp = list_art_rental_temp[0].replace("huurprijs:","")
			temp = temp.replace("p/m","")
			temp = temp.replace("aanbieding:","")
			temp = temp.rstrip(' ')
			temp = temp.lstrip(' ')
			rowtext['rental fee'] = temp.strip('\r\n\t').encode('utf-8')
		except:
			pass
		print rowtext
		writer.writerow(rowtext)
   
rowtext = {'gallery': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with codecs.open('artlinq_kunstcentrum.csv', 'wb') as csvfile:
	fieldnames = ['gallery', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print fieldname
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	#list_index = int(sys.argv[1])
	search_url =  "http://www.kunstcentrum.nl/kunstwerken/"
	print search_url
	try :
		page = 0
		write_scraped_data(search_url,writer, rowtext, fieldnames)
		search_url = search_url.rsplit('?', 1)[0]
		search_page = "?page="
		
		for i in range(2,12):
			page = i
			#list_index = list_index + 1
			search_page = search_page + str(page)
			current_search_url = search_url + search_page
			print current_search_url
			write_scraped_data(current_search_url,writer, rowtext, fieldnames)
			search_url = current_search_url.rsplit('?', 1)[0]
			search_page = "?page="
			
			
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]