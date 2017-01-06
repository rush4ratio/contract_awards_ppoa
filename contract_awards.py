import urllib2 
from datetime import datetime
import time
import ucsv as csv
import re
from bs4 import BeautifulSoup

def remove_date_suffixes(dt):
    return re.sub(r'(\d)(st|nd|rd|th)', r'\1', dt)

def tidy_date(dt):
    return datetime.strptime(remove_date_suffixes(dt), "%d, %B %Y").strftime('%m/%d/%y')


def parse_summary_row(row):
    award = {}
    td = row.find_all("td")

    if td:
        award["procuring_entity"] = td[0].a.get_text().strip()
        award["procurement_ref_no"] = td[1].get_text().strip()
        award["description"] = td[2].get_text().strip()
        award["contractor"] = td[3].get_text().strip()
        award["amount"] = td[5].get_text().strip().replace("KSH","")
        award["url_full"] = td[6].a.get('href')

    return award

def parse_full_row(item):
    award = {}
    tr = item.find_all("tr")

    if tr:
        award["procuring_method"] = tr[1].td.get_text().strip()
        award["advert_date"] = tidy_date(tr[5].td.get_text().strip())
        award["notification_date"] = tidy_date(tr[6].td.get_text().strip())
        award["contract_signing"] = tidy_date(tr[7].td.get_text().strip())
        award["completion_date"] = tidy_date(tr[8].td.get_text().strip())
        award["tenders_sold"] = tr[9].td.get_text().strip()
        award["bids_received"] = tr[10].td.get_text().strip()

    return award

def url2soup(link):
    html = urllib2.urlopen(link)    
    soup = BeautifulSoup(html, "lxml")
    return soup


BASE_URL = 'http://supplier.treasury.go.ke'



# Open our CSV file and write the headers
now = datetime.now()
csvfilename = "contract_awards-" + now.strftime("%Y%m%d-%H_%M_%S") + ".csv"
csvfile = open(csvfilename, "wb")
aw_writer = csv.writer(csvfile)
aw_writer.writerow(['procuring_entity', 'procurement_ref_no', 'description', 'contractor', 'amount', 'procuring_method', 'advert_date', 'notification_date', 'contract_signing', 'completion_date', 'tenders_sold', 'bids_received'])

start_time = time.time()

awards_scraped = 0


for counter in xrange(1,129): # 129 for all pages
    # Fetch page
    soup = url2soup("http://supplier.treasury.go.ke/site/tenders.go/index.php/public/contracts/page:"+str(counter))
    print "Looking at page " + str(counter)

    rows = soup.find("table", class_="table-striped").find_all("tr")

    for row in rows:
        award = parse_summary_row(row)

        if(award):
            soup = url2soup(BASE_URL + award["url_full"])
            print("Reading " + award["procurement_ref_no"] + " in detail...")
            item = soup.find("table", class_="table-striped")
            
            award.update(parse_full_row(item))

            aw_writer.writerow([award["procuring_entity"],award["procurement_ref_no"],award["description"],\
                                award["contractor"], award["amount"], award["procuring_method"],\
                                award["advert_date"], award["notification_date"],\
                                award["contract_signing"], award["completion_date"], award["tenders_sold"], \
                                award["bids_received"] ])

            print "Award written"

            awards_scraped += 1

csvfile.close()
print("Contract awards scraped: "+ str(awards_scraped))
