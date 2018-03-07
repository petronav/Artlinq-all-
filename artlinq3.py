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
   
"""
rowtext = {'kunstuitleen': '', 'kunstenaar': '', 'titel':'', 'technique':'', 'subject': '', 'size': '', 'orientation':'', 'color': '', 'price':'', 'rental fee': '', 'availability':''}
with open('artlinq.csv', 'w') as csvfile:
	fieldnames = ['kunstuitleen', 'kunstenaar', 'titel', 'technique', 'subject', 'size', 'orientation', 'color', 'price', 'rental fee', 'availability']
	for fieldname in fieldnames:
		print(fieldname)
	
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	search_url =  u2.unquote(u2.unquote(sys.argv[1]))
"""	
response  = requests.get(search_url, timeout=30)
#print(response)

#while response.status_code == 200 :
data = response.text.encode('utf-8')
parsed_body = html.fromstring(data)
print(parsed_body)
list_arts = parsed_body.xpath('//div[@class="pod-inner"]')
print("num artwork masonry", len(list_arts))
list_load_more = parsed_body.xpath('//div[@class="plp-pod__image"]')
print("list_load_more",len(list_load_more))
list_exact = parsed_body.xpath('//a[@class="js-podclick-analytics"]/@href')
print("list_exact",len(list_exact))
count = 0

for i in list_exact:
	#print(i)
	rspns  = requests.get(base_url+i, timeout=30)
	#print(response)
	dta = rspns.text.encode('utf-8')
	prsd_bd = html.fromstring(dta)
	min_div = prsd_bd.xpath('//div[@class="media__main-image"] ')
	min_img = prsd_bd.xpath('//img[@id="mainImage"]/@src')
	print(min_img)
	count+=1
	for j in min_img:
		r = requests.get(j)
		with open("prod"+str(count)+".jpg","wb") as code:
			code.write(r.content)

"""
if (len(list_load_more)>0):
	new_search_url = search_url + "/unknown" + list_load_more[0]
else:
	new_search_url = search_url + "/unknown"
print("new search url", new_search_url)
response  = requests.get(new_search_url, timeout=30)
print("status code", response.status_code)
"""