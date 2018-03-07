import sys
from lxml import html
from lxml import etree
import requests
from urllib3 import request
import csv
search_url = "https://www.homedepot.com/b/Tools-Hand-Tools-Pliers-Locking-Pliers/N-5yc1vZcbrp"
base_url = "https://www.homedepot.com"
def write_scraped_data( search_url,writer, rowtext, fieldnames ):
	response  = requests.get(search_url, timeout=30)
	data = response.text.encode('utf-8')
	parsed_body = html.fromstring(data)
	list_arts = parsed_body.xpath('//div[@class="pod-inner"]')
	print("num arts", len(list_arts))
	for cur_art in list_arts:
		parsed_art = html.fromstring(cur_art)
		list_a = parsed_body.xpath('//a/@href')
		print("num a", len(list_a))
response  = requests.get(search_url, timeout=30)
data = response.text.encode('utf-8')
parsed_body = html.fromstring(data)
list_arts = parsed_body.xpath('//div[@class="pod-inner"]')
list_load_more = parsed_body.xpath('//div[@class="plp-pod__image"]')
list_exact = parsed_body.xpath('//a[@class="js-podclick-analytics"]/@href')
count = 0
for i in list_exact:
	rspns  = requests.get(base_url+i, timeout=30)
	dta = rspns.text.encode('utf-8')
	prsd_bd = html.fromstring(dta)
	thmb_div = prsd_bd.xpath('//div[@id="overlayThumbnails"] ')
 	thmb_lnk = prsd_bd.xpath('//a[@class="overlayThumbnail overlayThumbnail--selected"]/@href')
	thmb_img = prsd_bd.xpath('//img/@src')
	thmb_img2=[]
	for j in thmb_img:
		if j.startswith('https'):
			if j[-7:].startswith('145'):
				j = j[:-7]
				j = j + '1000.jpg'
				thmb_img2.append(j)
	print(thmb_img2)
	count+=1
	
	for m in thmb_img2:
		r = requests.get(m)
		with open("prod"+str(count)+".jpg","wb") as code:
			code.write(r.content)