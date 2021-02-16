#!/usr/bin/env python
# coding: utf-8

# import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium import webdriver
import pymongo
from splinter import Browser
#chrome_options = webdriver.ChromeOptions() 
#chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
#driver = webdriver.Chrome(options=chrome_options)  
from webdriver_manager.chrome import ChromeDriverManager

#options = webdriver.ChromeOptions() 
#options.add_experimental_option("excludeSwitches", ["enable-logging"])
##driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
#driver.get("https://www.google.com/")

def scrape():  
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

    #browser = browser_set()
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Retrieve page with the requests module
    # response = requests.get(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')


    # Retrieve article title from web page.
    title = soup.find('div', class_='list_text').find('a').text
    # title_main = title[0].text.strip()
    title

  # Retrieve article 
    newpara = soup.find('div', class_='article_teaser_body').text
    # newpara_main = newpara[0].text.strip()
    newpara


    # ### Mars Facts

    url2 = "https://space-facts.com/mars/"


    # Reading table from web page
    tables = pd.read_html(url2)


    # Coverting table into dataframe
    mars_df = tables[0]
    mars_df.head()

    # Add column headers
    mars_df.columns = ['Description', 'Facts']
    mars_df

    # Convert to HTML
    mars_df_html = mars_df.to_html()
    mars_df_html

    # Stripping unwanted newlines to clean up the table
    mars_df_table = mars_df_html.replace('\n','')
    mars_df_table

    # Saving table directly to a file
    mars_df.to_html('mars_table.html')

    # ### Mars Hemispheres

    # Set up URL links
    main_url = 'https://astrogeology.usgs.gov'
    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_url)

    # Create HTML object to be parsed
    hemi_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(hemi_html, 'html.parser')

    results = soup.find('div', class_='collapsible results')
    items = results.find_all('div', class_='item')

    pic_url = []

    for item in items:
        title = item.find('h3').text
        img_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + img_url)
        pic_html = browser.html
        soup = bs(pic_html, 'html.parser')
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        pic_url.append({'title':title, 'img_url':img_url})

    for pic in range(len(pic_url)):
        print(pic_url[pic]['title'])
        print(pic_url[pic]['img_url'])

    pic_1 = {'title': pic_url[0], 'img_url':pic_url[0]}
    pic_2 = {'title': pic_url[1], 'img_url':pic_url[1]}
    pic_3 = {'title': pic_url[2], 'img_url':pic_url[2]}
    pic_4 = {'title': pic_url[3], 'img_url':pic_url[3]}

    allimage_url = [pic_1, pic_2, pic_3, pic_4]

    main_info = {}
    main_info['title'] = title
    main_info['newpara'] = newpara
    main_info['mars_df_html'] = mars_df_html
    main_info['allimage_url'] = allimage_url

    browser.quit()

    return main_info
