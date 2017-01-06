import urllib2 
from datetime import datetime
import time
import ucsv as csv
import re
from bs4 import BeautifulSoup

def url2soup(link):
    html = urllib2.urlopen(link)    
    soup = BeautifulSoup(html, "lxml")
    return soup

def get_row_info(cell):
    pe = {}
    if(cell.findAll('a')):
        pe["name"] = cell.findAll('a')[1].get_text().strip().upper()
        pe["type"] = cell.findAll('a')[2].get_text().strip()    

    return pe

BASE_URL = 'http://supplier.treasury.go.ke/site/tenders.go/index.php/public/entities/page:'

now = datetime.now()
csvfilename = "procuring-entities-" + now.strftime("%Y%m%d-%H_%M_%S") + ".csv"
csvfile = open(csvfilename, "wb")
writer = csv.writer(csvfile)
writer.writerow(['name','type'])

pes_scraped = 0 

for page_num in xrange(1,30):
    print "Reading page" + str(page_num) + "..."
    soup = url2soup(BASE_URL + str(page_num))
    table_cells = soup.findAll('table',{'class':'procuring-entities'})[1].find_all('td')    

    for cell in table_cells:
        pe = get_row_info(cell)

        if(pe):
            writer.writerow([pe["name"], pe["type"]])
            print pe["name"] + " written"
            pes_scraped += 1

csvfile.close()
print("PEs scraped: "+ str(pes_scraped))
