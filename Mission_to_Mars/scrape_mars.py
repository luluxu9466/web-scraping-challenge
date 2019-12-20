from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

    browser = init_browser()

    nasa_url = "https://mars.nasa.gov/news"
    # Visit NASA
    browser.visit(nasa_url)  

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all('div', class_ = 'content_title')
    text = soup.find_all('div', class_='article_teaser_body')

    # Assign title and text to variables that you can reference later.
    news_title = title[0].get_text()
    news_p = text[0].get_text()

    # Close the browser after scraping
    browser.quit()

    browser = init_browser()

    # Visit jpl
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)  
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured = soup.find_all('article', class_='carousel_item')

    # Assign the url string to a variable called featured_image_url.
    featured_image = featured[0]["style"].strip("'background-image: url(").strip("');'")
    featured_image_url = 'https://www.jpl.nasa.gov/'+featured_image

    # Close the browser after scraping
    browser.quit()

    # Scrape weather data from Twitter
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    twitter = soup.find('div', class_='js-tweet-text-container')
    mars_weather= twitter.get_text()

    # Scrape mars information table
    planet_url = "https://space-facts.com/mars/"
    tables = pd.read_html(planet_url)
    df = tables[0]
    df.rename(columns = {0:"description", 1: "value"}, inplace = True)
    planet_html = df.to_html(index=False)

    # Get hemisphere image urls
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(astro_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    download = soup.find_all('a', class_="itemLink product-item")
    usgs_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []

    for i in range(len(download)):
        image_url = usgs_url + download[i]["href"]
        response = requests.get(image_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        image = soup.find('li')
        img_url = image.find("a")["href"]
        hemisphere_image_urls.append({"title": download[i].get_text(),
                                    "img_url": img_url})

    # Store data in a dictionary
    data = {"news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        'mars_weather': mars_weather,
        'planet_html': planet_html,
        'hemisphere_image_urls': hemisphere_image_urls
        }

    return data
