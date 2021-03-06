
# import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def browser_init():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = browser_init()
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Retrieve page with the requests module
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Retrieve article title from web page.
    title = soup.find('div', class_='list_text').find('a').text

  # Retrieve article 
    newpara = soup.find('div', class_='article_teaser_body').text


    # ### Mars Facts
    url2 = "https://space-facts.com/mars/"

    # Reading table from web page
    tables = pd.read_html(url2)

    # Coverting table into dataframe
    mars_df = tables[0]

    # Add column headers
    mars_df.columns = ['Description', 'Facts']

    # Convert to HTML
    mars_df_html = mars_df.to_html()

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


    main_info = {'title':title}
    main_info[newpara]=newpara
    main_info['mars_df_html']=mars_df_html
    main_info['pic_url']=pic_url

    browser.quit()

    return main_info