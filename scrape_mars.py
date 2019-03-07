from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import os
import pandas as pd 
import pprint
import pymongo

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)
db = client.mars_db
# db.news.drop()
# db.imageurl.drop()
# db.marsweather.drop()
# db.mars_info.drop()
# db.mars_hemispheres.drop()

def scrape():

    url = 'https://mars.nasa.gov/news/'
    browser = Browser('chrome')
    browser.visit(url)
    html = browser.html


    soup = bs(html, 'lxml')


    #title of first article
    title = soup.find('div', class_='content_title')
    time.sleep(2)
    news_title = title.text
    print(news_title)

    #paragraph text of first article
    para = soup.find('div', class_='article_teaser_body')
    time.sleep(2)
    new_para = para.text
    print(new_para)
    news = {'title': news_title, 'paragraph': new_para}


    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&q=Mars'
    browser.visit(url2)
    time.sleep(2)

    browser.click_link_by_id("full_image")
    time.sleep(2)
    html2 = browser.html


    soup2 = bs(html2, 'lxml')
    #soup2


    imagediv = soup2.find('img', class_="fancybox-image")['src']
    imagediv


    featured_image_url = 'https://www.jpl.nasa.gov' + imagediv
    print(featured_image_url)
    imageurl = {'featured_image': featured_image_url}


    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html


    soup3 = bs(html3, 'lxml')


    weather = soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = weather.text
    print(mars_weather)
    marsweather = {'weather': mars_weather}


    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)
    html4 = browser.html


    soup4 = bs(html4, 'lxml')



    tables = pd.read_html(html4)
    info_table = tables[0]
    mars_info = {'table': info_table.to_html()}


    def retrieve_hemis():
        # URL for USGS Astrogeology
        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        
        # Visit URL and parse html
        browser.visit(url5)
        html5 = browser.html
        soup5 = bs(html5, 'lxml')
        
        # find the articles
        articles = soup5.find_all('div', class_='description')[0:4]
        
        # create list object to store output
        imgs = []
        
        # iterate over articles
        for article in articles:
            img = {}
            href = article.h3.text
            browser.click_link_by_partial_text(href)
            html5 = browser.html
            soup5 = bs(html5, 'lxml')
            img['title'] = href
            img['img_url'] = soup5.find('a', target='_blank')['href']
            imgs.append(img)
            
            #restart process
            browser.visit(url5)
            
        return(imgs)

    imgs = retrieve_hemis()


    print(imgs)


    db.news.insert(news)
    db.imageurl.insert(imageurl)
    db.marsweather.insert(marsweather)
    db.mars_hemispheres.insert_many(imgs)
    db.mars_info.insert(mars_info)

#scrape()