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
 
   
rowtext = {'gallery': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with codecs.open('artlinq_art4u.csv', 'wb', 'utf-8') as csvfile:
	fieldnames = ['gallery', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	#unicodeW = UnicodeDictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	
	search_url =  "http://www.art4u.nl/particulier/bekijk-collectie/"
	#print search_url
	try :
		response  = requests.get(search_url, timeout=60)
		data = response.text.encode('utf-8')
		parsed_body = html.fromstring(data)
		list_iframe_url = parsed_body.xpath('//iframe/@src')
		print list_iframe_url
		form_data = {'HAE': '1', 'HKT': 'P', 'KS1': 'checked', 'KS2':'checked', 'KS3': 'checked', 'KF1': 'checked', 'KF2': 'checked', 'KF3': 'checked', 'NAAM': '', 'KC1': 'checked', 'KC2': 'checked', 'KC3':'checked', 'Bek':'Bekijken', 'Vor':'Vorige pagina', 'Vol':'Volgende pagina'}
		response  = requests.get(list_iframe_url[0], timeout=60)
		data = response.text.encode('utf-8')
		#print data
		parsed_body = html.fromstring(data)
		#list_size = parsed_body.xpath('//div[@id="wrapper"]/font/br[1]/text()')
		list_size = parsed_body.xpath('//body/script')
		temp_text = etree.tostring(list_size[0], pretty_print=True)
		print temp_text
		#m = re.findAll("\Array", temp_text)
		#if m:
		#	print m.group(1)
		for curText in temp_text.split('&#13'):
			if ',' in curText and 'Array' in curText: 
				curText = curText.split(',')
				print
				try:
					#print curText[3]
					rowtext['kunstenaar'] = curText[3].strip('\r\n\t').encode('utf-8')
					rowtext['kunstenaar'] = rowtext['kunstenaar'].replace("-","")
					rowtext['kunstenaar'] = rowtext['kunstenaar'].replace("\"","")
					print rowtext['kunstenaar']
				except:
					pass
				try:
					#print curText[4]
					nChar = len(curText[4])
					rowtext['titel'] = curText[4][:nChar-2].strip('\r\n\t').rstrip('\)').encode('utf-8')
					rowtext['titel'] = rowtext['titel'].replace("-","")
					rowtext['titel'] = rowtext['titel'].replace("\"","")
					print rowtext['titel']
				except:
					pass
				try:
					#print curText[2]
					rowtext['size'] = curText[2].strip('\r\n\t').encode('utf-8')
					rowtext['size'] = rowtext['size'].replace("-","")
					rowtext['size'] = rowtext['size'].replace("\"","")
					print rowtext['size']
				except:
					pass
				print rowtext
				rowtext['gallery'] = "ART4U"
				writer.writerow(rowtext)
					
		csvfile.close()
	except:
		print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]