#!/usr/bin/env python
# coding: utf-8

# In[47]:


#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd
import time


# In[6]:

def scrape():
    # URL of page to be scraped
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    url = "https://redplanetscience.com"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    (soup.prettify(), 'mars_news_site')


    # In[7]:


    #scrape the article title
    news_title = soup.select_one('.content_title').text
        
    # scrape the article subheader
    news_p = soup.select_one('.article_teaser_body').text

    # print article data
    print('-----------------')
    print(news_title)
    print(news_p)

    # # Dictionary to be inserted into MongoDB
    # post = {
    #     'title': news_title,
    #     'news text': news_p,
    # }

    # # Insert dictionary into MongoDB as a document
    # collection.insert_one(post)


    # In[20]:


    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Assign new URL
    url2 = "https://spaceimages-mars.com/"

    browser.visit(url2)


    #Scrape page to get feature image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find_all('div', class_='header')

    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url2 + relative_image_path

    browser.quit()

    #Seeing if the URL is correct
    print(featured_image_url)


    # In[25]:


    #New URL for Mars Facts
    url3 = "https://galaxyfacts-mars.com"

    #Using Pandas to read table
    tables = pd.read_html(url3)
    tables


    # In[32]:


    df = tables[0]
    df.head()


    # In[33]:


    # Convert table to HTML Table String
    html_table = df.to_html()
    html_table


    # In[34]:


    #remove unwanted newlines from the string of code
    html_table = html_table.replace('\n', '')

    #edit table with BeautifulSoup
    soup2 = BeautifulSoup(html_table,"lxml")
    soup2.find("table")['class']='table table-striped'

    #convert BeautifulSoup back to html
    html_table = str(soup2)

    print(f'This is our {html_table}.')

    # In[63]:


    #obtain the HQ images of Mar's hemispheres

    #empty list of soon-to-be-dictionaries
    hemisphere_image_urls = []

    # Get a List of All the Hemispheres



    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    url4 = "https://marshemispheres.com"
    driver.get(url4)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    l=driver.find_elements_by_tag_name('a')

    #filtering html to get to the links we want
    filtered_links = []
    for element in l:
        href=element.get_attribute('href')
        if '.html' in href:
            filtered_links.append(href)

    #go through filtered links to get HQ picture
    for f_link in filtered_links:
        driver.get(f_link)
        HQ_pic = driver.find_elements_by_tag_name('a')
        #create an empty dictionary
        data = {}
        #setting up img_url by getting ahh
        for a in HQ_pic:
            ahh= a.get_attribute('href')
            if 'full.jpg' in ahh:
                data['img_url']=ahh
                break
        #setting up title by getting title        
        title_att = driver.find_element_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2')
        title = title_att.text
        data ['title']=title
        #append dictionary to list    
        hemisphere_image_urls.append(data)

    driver.quit()
    #remove possible duplicates values
    hemisphere_image_urls = {frozenset(item.items()) : item for item in hemisphere_image_urls}.values()
    hemisphere_image_urls_list=list(hemisphere_image_urls)
    print(hemisphere_image_urls_list)


    final_items = {
        'news_title':news_title,
        'news_p':news_p,
        'feat_img_url':featured_image_url,
        'html_table':html_table,
        'hemi_img_url':hemisphere_image_urls_list
    }
    return final_items





