
from bs4 import BeautifulSoup

import requests
from mongoengine import *
import logging


LOG_FILENAME = '/var/log/mongodb/flipkart.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )



class Page(Document):
    db_brand_name = StringField()
    db_title = StringField()
    db_url = StringField()
    db_page_source = StringField()


connect('flipkart1')


url1 = []
alist = []
url1 = ["http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B2001%2B-%2BRs.%2B5000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B5001%2B-%2BRs.%2B10000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B10001%2B-%2BRs.%2B18000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B18001%2B-%2BRs.%2B25000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B25001%2B-%2BRs.%2B35000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B35001%2Band%2BAbove&sid=tyy,4io"]



def Dat(link):
     try:
        s1 = requests.get(link)
        plain_text1 = s1.text
        soup1 = BeautifulSoup(plain_text1)
        title=soup1.find("h1").text
        #location = soup1.find('span', {'class': 'selling-price omniture-field'}).text
        brand1 = soup1.find_all('a',{'class':'link fk-inline-block'})
        print link
        print title
        #print location
        try:
            brand=str(brand1[3].text).strip()[0:-7]
            print brand
            Page(db_brand_name=str(brand1), db_title=str(title), db_url=link,
                     db_page_source=plain_text1.encode('utf-8')).save()
            logging.info("\n*****"+str(title)+"Successfully added to database*****\n")

        except:
            logging.error(errors)
            print " "
        print "-------------"
     except:
        print "error1"
        logging.error(errors)



def find(urls):
     j=0
     while True:
       try:
        s = requests.get(urls)
        plain_text = s.text
        soup = BeautifulSoup(plain_text)
        nnextURL=""
        nextURL = soup.findAll('a', {'class': 'next'})
        print nextURL
        if not nextURL:
            break
        else:
            urls="http://flipkart.com"+nextURL[0].get('href')
            nextURL=[]
            #print urls
        for links in soup.findAll('a', {'class': 'fk-display-block'}):
            v=links.get('href')
            j=j+1
            print j

            v2="http://www.flipkart.com"+v
            print v2
            Dat(v2)
       except:
        print "error"


for urls in url1:
   find(urls)
