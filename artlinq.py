import urllib2
import sys
import csv
from bs4 import BeautifulSoup
import requests

def check_site(site, cursite, validsites):
	retval = 0
	#print "check_site", cursite
	try:
		#response  = requests.get(cursite)
		response  = requests.get(cursite, timeout=30)
		data = response.text
		code = response.status_code
		redirect_url = response.url
		print site
		print cursite
		print code
		print redirect_url
		#print data
		if code==200:
			if "404" in redirect_url:
				validsites.append((site, (cursite,"invalid")))
			elif "not found" in redirect_url:
				validsites.append((site, (cursite,"invalid")))
			elif "error" in redirect_url:
				validsites.append((site, (cursite,"invalid")))
			elif redirect_url == site :
				print "redirect_url is base url"
				validsites.append((site, (cursite,"invalid")))
			else:
				soup = BeautifulSoup(data)
				for div_tag in soup.find_all('div'):
					if div_tag.text == "This domain may be for sale.":
						print "This domain is for sale"
						validsites.append((site, (cursite,"invalid")))
						return 0
				retval = 1
				validsites.append((site, (cursite,"valid")))
	except:
		validsites.append((site, (cursite,"invalid")))
		print "Unexpected error3:", sys.exc_info()[0]
	return retval
start_index = int(sys.argv[1])
end_index = int(sys.argv[2])

	

	
outfilename = "fjsites";
infilename = "sites";
curoutfilename = "";
curinpfilename = "";
for i in range(start_index,end_index):
	if i < 10:
		curoutfilename = outfilename + "_00" + str(i) + ".csv";
		curinpfilename = infilename + "_00" + str(i) + ".txt";
	elif i < 100:
		curoutfilename = outfilename + "_0" + str(i) + ".csv";
		curinpfilename = infilename + "_0" + str(i) + ".txt";
	else :
		curoutfilename = outfilename + "_" + str(i) + ".csv";
		curinpfilename = infilename + "_" + str(i) + ".txt";

	with open(curinpfilename, "r") as ins:
		sites = []
		for line in ins:
			line = line.strip()
			sites.append(line)

			
	validsites = []
	link_found = 0
	httpget_timeout=60
	counter = 0
	for site in sites:
		site.rstrip('\n')
		if not site:
			pass
		link_found = 0
		try :
			print "current counter", counter, site
			counter = counter +1
			#r  = requests.get(site) #rishi "http://" +
			response  = requests.get(site, timeout=30)
			data = response.text

			soup = BeautifulSoup(data)
			ret_link = ""
			for link in soup.find_all('a'):
				#print link
				ret_link = link.get('href')
				if ret_link is not None and "/careers" in ret_link :
					if "http" not in ret_link :
						#for linkcode in validsites:
						#	print "linkcode", linkcode
						#	print "ret_link", site+ret_link
						if not any(site in linkcode for linkcode in validsites):
							#print site.encode('utf-8')+ret_link.encode('utf-8')
							validsites.append((site, (site+ret_link, "valid")))
							#print "retlink does not have http", validsites
					else:
						if not any(site in linkcode for linkcode in validsites):
							#print ret_link.encode('utf-8')
							validsites.append((site, (ret_link, "valid")))
							#print "retlink has http", validsites
					link_found = 1
				elif ret_link is not None and "/jobs" in ret_link :
					if "http" not in ret_link :
						if not any(site in linkcode for linkcode in validsites):
							#print site.encode('utf-8')+ret_link.encode('utf-8')
							validsites.append((site, (site+ret_link, "valid")))
							#print validsites
					else:
						if not any(site in linkcode for linkcode in validsites):
							#print ret_link.encode('utf-8')
							validsites.append((site, (ret_link, "valid")))
							#print validsites
					link_found = 1
			if link_found == 0:
			#	validsites.append((site,"invalid"))
				cursite = site + "/" + "jobs";
			#	print cursite;
			#	if(not check_site(site, cursite, validsites)):
			#		cursite = site + "/" + "careers";
			#		if(not check_site(site, cursite, validsites)):
			#			if ("http://www" in site):
			#				cursite = site.replace("http://www.", "http://careers.")
			#				#print "matched www", cursite
			#			elif ("https://www" in site):
			#				cursite = site.replace("https://www.", "https://careers.")
			#				#print "matched www", cursite
			#			elif ("http://" in site):
			#				cursite = site.replace("http://", "http://careers.")
			#				#print "matched", cursite
			#			elif ("https://" in site):
			#				cursite = site.replace("https://", "https://careers.")
			#				#print "matched", cursite
			#			if(not check_site(site, cursite, validsites)):
			#				if ("http://www" in site):
			#					cursite = site.replace("http://www.", "http://jobs.")
			#					#print "matched www", cursite
			#				elif ("https://www" in site):
			#					cursite = site.replace("https://www.", "https://jobs.")
			#					#print "matched www", cursite
			#				elif ("http://" in site):
			#					cursite = site.replace("http://", "http://jobs.")
			#					#print "matched", cursite
			#				elif ("https://" in site):
			#					cursite = site.replace("https://", "https://jobs.")
			#					#print "matched", cursite
			#				if(not check_site(site, cursite, validsites)):
			#					pass
		except:
			print site
			print "Unexpected error3:", sys.exc_info()[0], sys.exc_info()[1]
			validsites.append((site,("None","invalid")))
	with open(curoutfilename, 'w') as f:
		for site in validsites:
			f.write(site[0].encode('utf-8'))
			f.write(',')
			f.write(site[1][0].encode('utf-8'))
			f.write(',')
			f.write(site[1][1].encode('utf-8'))
			f.write('\n')
