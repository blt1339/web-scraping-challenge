from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pprint
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()


    #  Scrape the top Mars news story
    #-------------------------------------------------

    # Define Mars news url and visit it
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(5)

    # Create the HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the first article and information
    article = soup.find('div', class_='list_text')

    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text


    #  Scrape the feature image
    #-------------------------------------------------

    # Define the url and visit it 
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # Click on FULL IMAGE
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Click on more info
    browser.links.find_by_partial_text('more info').click()

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Get the largesize Mars Image
    img_info = soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov/{img_info}'

    #  Scrape the the Mars Facts
    #-------------------------------------------------

    # Define the facts url
    facts_url = 'https://space-facts.com/mars/'

    # Get the tables
    tables = pd.read_html(facts_url)

    # Pull the table we want from tables and store in DataFrame
    mars_facts_df = tables[0]

    # Update the column names
    mars_facts_df.columns = ['Description','Value']

    # Render DataFrame into HTML
    mars_html = mars_facts_df.to_html('mars-facts.html')


    #  Scrape the the Mars Hemisphere information
    #-------------------------------------------------
    
    # Define the hemisphere url and visit it
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # Create the HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve the first article and information
    hemisphere_info = soup.find('div', class_='collapsible results')

    # Retrieve the Mars hemisphere data
    mars_hemispheres = hemisphere_info.find_all('div', class_='item')

    # Loop through the retrieve hemisphere information extracting
    # the data we want

    # Initialize a list and base url
    hemisphere_image_urls = []
    usgs_url = 'https://astrogeology.usgs.gov/'

    
    for hemisphere in mars_hemispheres:

        # Retrieve the hemisphere title
        hemisphere_title = hemisphere.find('h3').text

        # Create the full url for the image and visit
        full_hemisphere_url = usgs_url + hemisphere.a['href']
        browser.visit(full_hemisphere_url)
    
        # Create the HTML object
        single_hemisphere_html = browser.html
    
        # Parse HTML with Beautiful Soup
        single_hemisphere_soup = BeautifulSoup(single_hemisphere_html, 'html.parser')
        single_hemisphere_info = single_hemisphere_soup.find('div', class_='downloads')
        single_hemisphere_url = single_hemisphere_info.find('li').a['href']
    
        # Create a dictionary to store in our list
        hemisphere_dict = {
                           'title': hemisphere_title,
                           'img_url':single_hemisphere_url
                          }
        # Update the list
        hemisphere_image_urls.append(hemisphere_dict)


        # Create a dictionary with the data
        mars_dict = {
                    "news_title": news_title,
                    "news_p": news_p,
                    "featured_image_url": featured_image_url,
                    "fact_table": str(mars_html),
                    "hemisphere_images": hemisphere_image_urls
                    }

            # Close the browser after scraping
            browser.quit()

        return mars_dict
