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
	
	#list_art_title = parsed_body.xpath('//div[@class="feat left"]/p/br[1]/text()')
	list_art_title = parsed_body.xpath('//div[@id="kunstdetail"]/img/@alt')
	print list_art_title
	#list_artist = parsed_body.xpath('//nav[@id="breadcrum"]/ul/li[3]/a/text()')
	#print list_artist
	list_data = parsed_body.xpath('//div[@class="feat left"]/p/text()')
	print list_data
	#list_size = parsed_body.xpath('//div[@class="feat left"]/p/br[3]/text()')
	#print list_size
	#list_price = parsed_body.xpath('//div[@class="feat left"]/p/br[4]/text()')
	#print list_price
	list_rental = parsed_body.xpath('//table/tr[3]/td[2]/text()')
	print list_rental
	#list_availability = parsed_body.xpath('//section[@id="artworkCentered"]/figure/figcaption/p/span[4]/text()')
	#print list_availability
	try:
		rowtext['kunstenaar'] = cur_artist.strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:
		rowtext['titel'] = list_art_title[0].strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:
		rowtext['technique'] = list_data[2].strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:
		rowtext['size'] = list_data[3].strip('\r\n\t').encode('utf-8')
	except:
		pass
	try:		
		rowtext['price'] = list_data[4].strip('\r\n\t').encode('utf-8')
		rowtext['price'] = rowtext['price'].replace("Prijs (incl. lijst):","")
	except:
		pass
	try:		
		rowtext['rental fee'] = list_rental[0].strip('\r\n\t').encode('utf-8')
	except:
		pass
	
	rowtext['kunstuitleen'] = "KUNSTUITLEEN MAASTRICHT"
	print rowtext
	writer.writerow(rowtext)
   
rowtext = {'kunstuitleen': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with codecs.open('artlinq_kunstuitleenmaastricht.csv', 'wb', 'utf-8') as csvfile:
	fieldnames = ['kunstuitleen', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print fieldname
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	#unicodeW = UnicodeDictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	
	search_url =  "http://www.kunstuitleenmaastricht.nl/collectie"
	print search_url
	try :
		response  = requests.get(search_url, timeout=60)
		data = response.text.encode('utf-8')
		parsed_body = html.fromstring(data)
		list_art_url = parsed_body.xpath('//div[@class="result"]/a[1]/@href')
		list_artist = parsed_body.xpath('////div[@class="result"]/a[2]/text()')
		cur_index = 0
		num_arts = len(list_art_url)
		print num_arts
		#while num_arts > 0:
		art_url = search_url.split('/')
		print art_url 
		for arturl in list_art_url:
			cur_art_url = art_url[0] + "//" + art_url[2] + arturl
			cur_artist = list_artist[cur_index]
			cur_index = cur_index + 1
			print cur_art_url
			artwork_response  = requests.get(cur_art_url, timeout=60)
			artwork_data = artwork_response.text.encode('utf-8')
			#print artwork_data
			artwork_parsed_body = html.fromstring(artwork_data)
			list_artwork_url = artwork_parsed_body.xpath('//div[@class="result"]/a[1]/@href')
			print list_artwork_url
			for artworkurl in list_artwork_url:
				cur_artwork_url = art_url[0] + "//" + art_url[2] + artworkurl
				print cur_artwork_url
				write_scraped_data(cur_artwork_url, writer, rowtext, fieldnames, cur_artist)
			# list_artwork_pages = artwork_parsed_body.xpath('//nav[@id="pagination"]/a[3]/text()')
			# if(len(list_artwork_pages) > 0):
				# print list_artwork_pages
				# num_pages = int (list_artwork_pages[0])
				# for cur_page in range(2,num_pages+1):
					# cur_art_url = cur_artwork_url + "?page=" + str(cur_page)
					# artwork_response  = requests.get(cur_art_url, timeout=60)
					# artwork_data = artwork_response.text.encode('utf-8')
					# artwork_parsed_body = html.fromstring(artwork_data)
					# #list_artwork_url = parsed_body.xpath('//ul[@class="artworksList"]/li/figure/a/@href')
					# list_artwork_url = parsed_body.xpath('//section[@id="artistArtworks"]')
					# print list_artwork_url
					# for artworkurl in list_artwork_url:
						# cur_artwork_url = art_url[0] + "//" + art_url[2] + artworkurl
						# write_scraped_data(cur_artwork_url,writer, rowtext, fieldnames, cur_artist)
				
			#write_scraped_data(cur_artwork_url,writer, rowtext, fieldnames)
			#list_next_url = parsed_body.xpath('//a[@class="kh-button uk-align-right button"]/@href')
			#print list_next_url
			#next_url = list_next_url[0] #"/index.php?option=com_kh&amp;task=ajax.nextSetOfArt&amp;namespace=artwork_filter&amp;offset=0&amp;limit=12&amp;return=aHR0cDovL3d3dy5rdW5zdGh1aXplbi5ubC9jb2xsZWN0aWUjZ3JpZC1hbmNob3I="
			
			#cur_search_url = data_url + next_url
			#response  = requests.get(cur_search_url, timeout=60)
			#data = response.text.encode('utf-8')
			#parsed_body = html.fromstring(data)
			#list_art_url = parsed_body.xpath('//div[@class="uk-width-1-4 artwork-item"]/figure/a/@href')
			#num_arts = len(list_art_url)
		csvfile.close()
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]