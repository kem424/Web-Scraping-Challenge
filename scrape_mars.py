#DEPENDENCIES
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time 
from flask import Flask, render_template
import pymongo
import time 

#DEFINE BROWSER
def browser():
    
    executable_path = {'/usr/local/bin/chromedriver'}
    return Browser('chrome', headless=False)  

def scrape():
    browser = Browser()
    mars_info = {}

    #NEWS
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_info["title"] = soup.find('div', class_="content_title").get_text()
    mars_info["body"] = soup.find('div', class_="rollover_description_inner").get_text()

    #IMAGE
    
    featured_image_url='https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA19039_hires.jpg'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    for x in range(50):
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('a',class_="button fancybox")

    for article in articles:
        img= article['data-fancybox-href']
        featured_image_url= 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA19039_hires.jpg'+img

    mars_info["image"] = featured_image_url

    #MARS WEATHER
    
    twitter_url='https://twitter.com/marswxreport?lang=en'
    
    browser.visit(twitter_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles= soup.find_all('div', class_="js-tweet-text-container")
    for article in articles:
        mars_weather=article.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    

    #MARS FACTS
    
    facts_url="https://space-facts.com/mars/"
    mars_facts_tables = pd.read_html(facts_url)
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df.set_index('Description', inplace=True)
    mars_facts_html=mars_facts_df.to_html()
    mars_info['mars_facts_html'] = mars_facts_html

    

    #Mars Hemispheres 
    hemisphere_image_urls = []
    
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    soup = BeautifulSoup (html, 'html.parser')
     
    for x in range(4): 
        time.sleep(5)
        hemisphere = result.find('div', class_="description")
        title = hemisphere.h3.text
        ending_url = hemisphere.a["href"]    
        browser.visit(beginning_url + ending_url)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = image_url

    return mars_info
