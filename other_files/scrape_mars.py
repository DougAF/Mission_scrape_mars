#Python back end for Flask import scrape function

#imports from ipynb
from bs4 import BeautifulSoup as bs
import numpy as np
import requests
import os
import pandas as pd
import time
#import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

def scrape():
    #store urls from all 5 scrapes(list better?)
    url_s_1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    url_s_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_s_3 = "https://twitter.com/marswxreport?lang=en"
    url_s_4 = "https://space-facts.com/mars/"
    url_s_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
   
    #splinter browser
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    #get htmls and soup objects
    response1 = requests.get(url_s_1)
    response2 = requests.get(url_s_2)
    response3 = requests.get(url_s_3)
    response4 = requests.get(url_s_4)
    response5 = requests.get(url_s_5)

    soup1 = bs(response1.text, 'lxml')
    soup2 = bs(response2.text, 'lxml')
    soup3 = bs(response3.text, 'lxml')
    soup4 = bs(response4.text, 'lxml')
    soup5 = bs(response5.text, 'lxml')

    ####### scrape 1 #######
    browser.visit(url_s_1)
        #Init empty lists
    titles_list = []
    ptext_list = []
        #fetch lists of HTML data
    results_title = soup1.find_all('div',class_="content_title")
    results_p = soup1.find_all('div', class_='rollover_description_inner')

        #grab all paragraphs
    for paragraph in results_p:
        ptext_list.append(paragraph.text)

        #grab all titles
    for title in results_title:
        titles_list.append(title.text)
        #locate most recent
    latest_title = titles_list[0]
    latest_paragraph = ptext_list[0]

    ####### scrape 2 #######
    browser.visit(url_s_2)
       # wait 4 seconds for page loading
        #find the image url for the current Featured Mars Image
        # wait 3 seconds for page load
    browser.click_link_by_id('full_image')
    time.sleep(3)   
    #fetch HTML for list creation
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url_find = soup.find('img', class_ = 'fancybox-image')
        #combines root of url with new found 'Featured image'
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url_find['src']

    ####### scrape 3 #######
    browser.visit(url_s_3)
        #fetch HTML for list creation
    html = browser.html
    soup = bs(html, 'html.parser')
        #grab all tweets
    tweet_container_list = soup.find_all('div', class_ = 'js-tweet-text-container')

        #find latest tweet container
    tweet_container_list[0]
    tweets_list = []
    for tweet_container in tweet_container_list:
        tweets_list.append(tweet_container.p.text.replace('\n', ' ').split('hPapic.twitter.com/', 1)[0])
        #Store tweet
    mars_weather = tweets_list[0]

    ####### scrape 4 #######
    mars_facts_tables = pd.read_html(url_s_4)
        #grab table from list
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df.columns = ['Measurement', 'Value']
    mars_facts_df_indexed = mars_facts_df.set_index('Measurement')
    mars_facts_html = mars_facts_df_indexed.to_html()
    
    ####### scrape 5 #######
    browser.visit(url_s_5)
        #grab data connected to hemisphere 
    hemi_links_list_raw = soup5.find_all('a', class_ = 'itemLink product-item')
        # init title and link lists 
    hemi_links_title_list = []
    hemi_links_href_list = []
        # parse out title and image link 
    for link in hemi_links_list_raw:
        hemi_links_title_list.append(link.text)
        hemi_links_href_list.append(link['href'])
        #complete image URLs
    hemi_full_url_list = []
    url_root = 'https://astrogeology.usgs.gov'
    for url_tail in hemi_links_href_list:
        hemi_full_url_list.append(url_root + url_tail)
        #full resolution image urls
    hemi_jpg_list = []
    for url in hemi_full_url_list:
        response = requests.get(url)
        soup = bs(response.text,'html.parser')
        #fetch full image(class ="wide-image")
        wide_image = soup.find('img', class_ = 'wide-image')
        hemi_jpg_list.append(url_root + wide_image['src'])
        #clean up titles
    clean_titles_list = []
    for title in hemi_links_title_list:
        clean_titles_list.append(title.split('Enhanced')[0].strip())

        #Create one dict for each hemisphere 
    hemi_dict_list = []
    for i in range(len(clean_titles_list)):
        hemi_dict_list.append(dict(zip(clean_titles_list[i:i+1], hemi_jpg_list[i:i+1])))



    # return dictionary of all scraped data
    scrape_mars_dict = {
        "latest_title" : latest_title,
        "latest_paragraph" : latest_paragraph,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "mars_facts" : mars_facts_html,
        "hemisphere_dictionary" : hemi_dict_list
    }
    ####### Display in Terminal #######
    print('(((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))',
        "Scraping Complete")

    return(scrape_mars_dict)


scrape()


