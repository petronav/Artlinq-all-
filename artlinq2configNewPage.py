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

list_Params = []
list_index = 0
num_pages = []
with open('artlinq_config.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		print(row['url'], row['iframe'], row['xpath1'], row['kunstenaar'], row['titel'], row['technique'], row['size'], row['availability'], row['price'], row['rental'], row['gallery'], row['numpages'], row['pagetag'], row['pagesupptag'],row['kunstenaarxpath'],row['availabilityxpath'],row['techniquexpath'])
		list_Params.append(row)
		num_pages.append(row['numpages'])
	csvfile.close()

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
	response  = requests.get(search_url, timeout=30)
	data = response.text.encode('utf-8')
	parsed_body = html.fromstring(data)
	#list_arts = parsed_body.xpath('//div[@class="nietcompact"]')
	print list_Params[list_index]['xpath1']
	list_arts = parsed_body.xpath(list_Params[list_index]['xpath1'])
	print "num arts", len(list_arts)
	art_url = search_url.split('/')
	print art_url 
	for art in list_arts[0].findall('a'):
		match = re.search(r'href=[\'"]?([^\'" >]+)', etree.tostring(art, pretty_print=True))
		if match:
			a_url = match.group(0)
		a_url = a_url.split('"')[1]
		cur_art_url = art_url[0] + '//' + art_url[2] + a_url
		print cur_art_url
		response  = requests.get(cur_art_url, timeout=30)
		data = response.text.encode('utf-8')
		parsed_body = html.fromstring(data)
		list_artist = parsed_body.xpath('//div[@class="tekstblok"]/h2/text()')
		rowtext['kunstenaar'] = list_artist[0].encode('utf-8','ignore')
		parameters = parsed_body.xpath('//div[@class="tekstblok"]/p/text()')
		param_count = 0
		#print "line 66"
		for parameter in parameters:
			parameter = parameter.strip('\r\n\t ')
			if param_count == 0:
				rowtext['titel'] = parameter.encode('utf-8','ignore')
				#print "line 71"
			if param_count == 1:
				param = parameter.split('(')
				rowtext['technique'] = param[0].encode('utf-8', 'ignore')
				rowtext['size'] = param[1].rstrip(')').encode('utf-8','ignore')
				#print "line 76"
			if param_count == 2:
				temp = parameter.replace("Prijs","")
				rowtext['price'] = temp 
				#print "line 79"
			param_count = param_count + 1
		availability = parsed_body.xpath('//div[@class="tekstblok"]/p/span/text()')	
		rowtext['availability'] = availability[0].encode('utf-8','ignore')
		print "gallery"
		rowtext["gallery"] = list_Params[list_index]["gallery"]
		print rowtext["gallery"], fieldnames[0]
		print rowtext
		writer.writerow(rowtext)
   
rowtext = {'gallery': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with codecs.open('artlinq.csv', 'wb', 'utf-8') as csvfile:
	fieldnames = ['gallery', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print fieldname
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	#unicodeW = UnicodeDictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	list_index = int(sys.argv[1])
	search_url =  urllib.unquote(urllib.unquote(list_Params[list_index]['url']))
	print search_url
	try :
		response  = requests.get(search_url, timeout=30)
		data = response.text.encode('utf-8')
		parsed_body = html.fromstring(data)
		if list_Params[list_index]['iframe']:
			list_iframe = parsed_body.xpath(list_Params[list_index]['iframe'])
			if "http" not in list_iframe[0]:
				search_url = search_url.rsplit('/', 1)[0]
				search_url = search_url + "/" + list_iframe[0]
			else:
				search_url = list_iframe[0] + "/catalogus.asp?cat=1&compact=0"
		print "search url",search_url
		print "history",response.history
		print search_url
		response  = requests.get(search_url, timeout=30)
		#print "response code", response.status_code
		#print response
		data = response.text.encode('utf-8')
		#print data
		parsed_body = html.fromstring(data)
		list_script = parsed_body.xpath("//script/text()")
		#tag = etree.toString(list_script[0], pretty_print=True)
		temp = list_script[0].strip('\r\n')
		temp = re.search('location="(.+?)";', temp)
		if temp:
			search_url = search_url + temp.group(1)
		print "search url",search_url
		page = 0
		write_scraped_data(search_url,writer, rowtext, fieldnames)
		search_url = search_url.rsplit('?', 1)[0]
		#search_supp = "&Cat=1&Prcat=0&Beschikbaar=0&Compact=0&="
		search_supp = list_Params[list_index]['pagesupptag']
		#search_page = "?pag="
		search_page = list_Params[list_index]['pagetag']
		
		for i in range(2,int(num_pages[list_index]) + 1):
			page = i
			#list_index = list_index + 1
			search_page = search_page + str(page)
			current_search_url = search_url + search_page + search_supp
			print current_search_url
			write_scraped_data(current_search_url,writer, rowtext, fieldnames)
			#search_url = current_search_url.rsplit('?', 1)[0]
			search_page = list_Params[list_index]['pagetag']
			search_supp = list_Params[list_index]['pagesupptag']
		csvfile.close()
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]