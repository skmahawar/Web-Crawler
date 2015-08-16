#!/usr/bin/env python

from mongoengine import *
from bs4 import BeautifulSoup
import requests
import logging

#log file configuration
LOG_FILENAME = '/var/log/mongodb/ratings.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
)

#connect to database
connect('multi_rating')
class Page(Document):
    db_brand_name = StringField()
    db_rating = StringField()


#LIST OF SEED PAGES
url1 = []
alist = []
url1 = ["http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B2001%2B-%2BRs.%2B5000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B5001%2B-%2BRs.%2B10000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B10001%2B-%2BRs.%2B18000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B18001%2B-%2BRs.%2B25000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B25001%2B-%2BRs.%2B35000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B35001%2Band%2BAbove&sid=tyy,4io"]



def ggr(title):
    urls="https://www.google.co.in/search?q=rating "+str(title)+" out of 5 E&start="

    count=0
    while count<30:
        urls=urls+str(count)
        source_code = requests.get(urls)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        s=soup.find_all('div',{'class': 'f slp'})
        for x in s:
            try:
                x1=str(x)
                y = x1[75:-6]
                print y
                Page(db_brand_name=str(title),
                     db_rating=y).save()
                logging.info("\n*****"+str(title)+"Successfully added to database*****\n")
            except:
             logging.error(errors)
             count=count+1
             print count
             continue

        count=count+10


#gather names of the devies
def Dat(link):

        s1 = requests.get(link)
        plain_text1 = s1.text
        soup1 = BeautifulSoup(plain_text1)
        title=soup1.find("h1").text
        brand1 = soup1.find_all('a',{'class':'link fk-inline-block'})
        print title
        print str(brand1[3].text).strip()[0:-7]
        ggr(title)
        print "-------------"


#gather all url's
def find(urls):
   try:
     while True:
        s = requests.get(urls)
        plain_text = s.text
        soup = BeautifulSoup(plain_text)
        nextURL = soup.findAll('a', {'class': 'next'})
        if not nextURL:
            break
        else:
            urls="http://flipkart.com"+nextURL[0].get('href')
            nextURL=[]
        for links in soup.findAll('a', {'class': 'fk-display-block'}):
            v=links.get('href')
            v2="http://www.flipkart.com"+v
            Dat(v2)
   except:
       print


for urls in url1:
    find(urls)








