#!/usr/bin/env python

#import all necessary libraries
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
from mongoengine import *
import logging

#configuring the log file
LOG_FILENAME = '/var/log/mongodb/reviews_new.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
)

#list to store brand names
brands = []


#make connection to database
connect('gsmarena')


#define database structure
class Page(Document):
    db_brand_name = StringField()
    db_title = StringField()
    db_url = StringField()
    db_page_source = StringField()
    db_review = ListField()


#base url of the website to be crawled
base_url = "http://www.gsmarena.com/"


#function to find all the brands of phones present on the website


def find_brands():

    #make the soup
    url = base_url
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    #extract all anchor tags under brandmenu div
    try:
        brand_menu = soup.find('div', {'id': 'brandmenu'}).find('ul')
        for brand in brand_menu.find_all('a'):
            brand_url = base_url + str(brand.get('href'))
            brands.append(brand_url)
    except:
        logging.error("*****Error in Saving Brand Names*****")


#function to find all the mobiles from a maker


def makers(page,brand_title):
    try:
        url = page
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for div in soup.find_all('div', {'class': 'makers'}):
            for mobile in div.find_all('a'):
                mobile_url = base_url + mobile.get('href')
                source_code_mobile = requests.get(mobile_url)
                plain_text_mobile = source_code_mobile.text
                mobile_soup = BeautifulSoup(plain_text_mobile)
                mobile_title = str(mobile_soup.find('title'))[7:-36]
                print(mobile_title)
                review_url = mobile_url.split('-')
                review_url_ = review_url[0] + "-reviews-" + review_url[1]
                review_soup = BeautifulSoup(requests.get(review_url_).text)
                review = []
                review.append(requests.get(review_url_).text)
                review_div = (review_soup.find('div', {'class': 'nav-pages'})).find_all('a')
                if review_div:
                    href = base_url+str(review_div[-2].get('href'))
                    review_url = review_url_.split('.')
                    i = 2
                    while review_url_ != href:
                        try:
                            review_url_ = review_url[0]+"."+review_url[1]+"."+review_url[2]+"p"+str(i)+"."+review_url[3]
                            review.append(requests.get(review_url_).text)
                            i += 1
                        except:
                            i += 1
                logging.info("\n\n*****" + mobile_title + "specs successfully gathered*****")

                Page(db_brand_name=brand_title, db_title=mobile_title, db_url=mobile_url,
                     db_page_source=plain_text_mobile.encode('utf-8'), db_review=review).save()
                logging.info("\n*****" + mobile_title + " successfully saved in database*****\n")
    except:
        logging.error("*****database error*****")


#find all the brands
find_brands()
#print brands

#collect all pages of a particular brand
#and call maker function for each page
for brand in brands:
    pages = []
    url = brand
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    brand_title = str(soup.find('title'))[10:-14]
    print(brand_title)
    pages.append(url)
    pgs = soup.find('div', {'class': 'nav-items'})
    #to check whether there is only one page
    if pgs is not None:
        for page in pgs.find_all('a'):
            pages.append(base_url + str(page.get('href')))
    for page in pages:
        makers(page,brand_title)
