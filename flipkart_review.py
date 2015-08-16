#!/usr/bin/env python

from bs4 import BeautifulSoup

import requests
import logging

from mongoengine import *

# log file configuration
LOG_FILENAME = '/var/log/mongodb/flipkart_ratings.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
)

#connect to database
connect('flipkart_review')


class Page(Document):
    db_brand_name = StringField()
    db_rating = StringField()


url1 = []
alist = []
url1 = ["http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B2001%2B-%2BRs.%2B5000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B5001%2B-%2BRs.%2B10000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B10001%2B-%2BRs.%2B18000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B18001%2B-%2BRs.%2B25000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B25001%2B-%2BRs.%2B35000&sid=tyy,4io",
        "http://www.flipkart.com/mobiles/pr?p[]=facets.price_range%255B%255D%3DRs.%2B35001%2Band%2BAbove&sid=tyy,4io"]


def gotofull(link, flag, title):
    try:
        rates = []
        source_code = requests.get(link)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        if flag == 0:
            a = soup.find_all('a', {'class': 'lnkViewAll'})
            flag = 1
            newpage = "http://www.flipkart.com" + a[1].get('href')
            print newpage
        else:
            a = soup.find_all('a', {'class': 'nav_bar_next_prev'})
            if not a[-1]:
                return 1
            else:
                print "else part"
                print a[-1]
                newpage = "http://www.flipkart.com" + str(a[-1].get('href'))
                print "this is for newpage " + newpage
            Rdata = soup.find_all('span', {'class': 'review-text'})
            for rate in Rdata:
                print rate.text
                Page(db_brand_name=str(title),
                     db_rating=str(rate.text)).save()

                logging.info("\n*****" + str(title) + "Successfully added review to database*****\n")
        gotofull(newpage, flag, title)
    except Exception as e:
        logging.error(e)


def Dat(link):
    try:
        s1 = requests.get(link)
        plain_text1 = s1.text
        soup1 = BeautifulSoup(plain_text1)
        title = soup1.find("h1").text
        #location = soup1.find('span', {'class': 'selling-price omniture-field'}).text
        brand1 = soup1.find_all('a', {'class': 'link fk-inline-block'})
        flag = 0
        gotofull(link, flag, title)
        print link
        print title
        #print location
        try:
            print ""
            #print str(brand1[3].text).strip()[0:-7]
        except:
            print "brand name out of bound "
        print "-------------"
    except Exception as e:
        logging.error(e)


def find(urls):
    j = 0
    while True:
        s = requests.get(urls)
        plain_text = s.text
        soup = BeautifulSoup(plain_text)
        nextURL = soup.findAll('a', {'class': 'next'})
        print nextURL
        if not nextURL:
            break
        else:
            urls = "http://flipkart.com" + nextURL[0].get('href')
            nextURL = []
            #print urls
        for links in soup.findAll('a', {'class': 'fk-display-block'}):
            v = links.get('href')
            j = j + 1
            print j

            v2 = "http://www.flipkart.com" + v
            print v2
            Dat(v2)
        print "error"


for urls in url1:
    find(urls)
