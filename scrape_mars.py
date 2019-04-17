from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time
import os

def init_browser():
    executable_path = {"executable_path": "/Users/saikondrakunta/Downloads/new_chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars = {}

    #NASA Mars News Scrape
    url_mars = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url_mars)
    time.sleep(2)

    html_mars = browser.html
    soup_mars = BeautifulSoup(html_mars, 'lxml')

    news_title = soup_mars.find('div', class_='content_title').text
    news_paragraph = soup_mars.find('div', class_='article_teaser_body').text
    mars['news_title'] = news_title
    mars['news_paragraph'] = news_paragraph

    #JPL Image Scrape
    url_jpl= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    time.sleep(2)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'lxml')

    image_location = soup_jpl.find('div', class_='fancybox-inner').img["src"].strip()
    featured_image_url = 'https://www.jpl.nasa.gov/' + image_location
    mars["featured_image"]= featured_image_url

    #Twitter Mars Weather Scrape
    url_mars_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_mars_weather)
    time.sleep(2)

    html_mars_weather = browser.html
    soup_mars_weather = BeautifulSoup(html_mars_weather, 'lxml')

    mars_weather = soup_mars_weather.find('p', class_='tweet-text').text.replace('\n', '').split("pic")[0]
    mars["mars_weather"]= mars_weather

    #Mars Facts Scrape using pandas
    url_facts = 'https://space-facts.com/mars/'
    time.sleep(2)


    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ['title', 'value']
    df.set_index("title", drop=True)
    html_facts = df.to_html( index=False)
    mars_html_table = html_facts.replace('\n','')

    mars["mars_facts_table"]= mars_html_table
    

    #Mars Hemisphere Scrape
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    html_hemisphere = browser.html
    soup_hemisphere = BeautifulSoup(html_hemisphere, 'lxml')

    hemisphere_image_urls = []
    base_url = "https://astrogeology.usgs.gov"
    results = soup_hemisphere.find_all("div", class_="item")
    for result in results:
        image_url = result.find('a', class_='itemLink product-item')['href']
        hemi_url = base_url + image_url
        browser.visit(hemi_url)
        html_hemisphere = browser.html
        soup_hemisphere = BeautifulSoup(html_hemisphere, 'lxml')
        title = soup_hemisphere.find('h2', class_='title').text
        image_loc = soup_hemisphere.find('img', class_='wide-image')["src"].strip()
        image_dict = {"title": title, "img_url": image_loc}
        hemisphere_image_urls.append(image_dict)
    print(hemisphere_image_urls)

    mars["hemisphere_image_urls"]= hemisphere_image_urls
    return mars
if __name__ == "__main__":
    print(scrape())

