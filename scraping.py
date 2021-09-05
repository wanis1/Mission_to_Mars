
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere = scrape_hemisphere_data(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere
    }
     # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

     # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    return news_title, news_p


    # ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

 # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None   

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    
    return img_url



    # ## Mars Facts

def mars_facts():
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
      return None
    # Assign columns and set index of dataframe
    df.columns = ['description','Mars', 'Earth']
    df.set_index('description', inplace = True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#-----------------------------------------------

#SCRAPE THE HEMISPHERE DATA
def scrape_hemisphere_data(browser):
    from bs4 import BeautifulSoup
    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    hemisphere_image_text = []
    thumbnail_links = []

    html_ = browser.html
    soup = BeautifulSoup(html_, 'html.parser')

    # Write code to retrieve the image urls and titles for each hemisphere.
    results = soup.find_all('a', class_="itemLink")


    # Get text and store in list
    for i in [1,3,5,7]:
        hemispheres = results[i].find_all('h3')
        for name in hemispheres:
            hemisphere_image_text.append(name.text)
        
    hemisphere_image_text


    #getting links to thumbnails
    results = soup.find_all('a', class_="itemLink")
        
    for result in results:
        if (result.img):
            thumbnail_url = "https://marshemispheres.com/"+ result["href"]
            thumbnail_links.append(thumbnail_url)
                
    thumbnail_links
            

    #Full sized image
    from bs4 import BeautifulSoup 
    hemisphere_urls = []
    for link in thumbnail_links:
        browser.visit(link)
        
        html_ = browser.html
        soup = BeautifulSoup(html_, 'html.parser')
        
        results = soup.find_all('a')[3]
        
        img_url = "https://marshemispheres.com/" + results["href"]
        
        hemisphere_urls.append(img_url)
    hemisphere_urls
        
    # Print the list that holds the dictionary of each image url and title.
    for i in range(4):
        hemisphere_image_urls.append({'img_url' : hemisphere_urls[i], 
                                    'title': hemisphere_image_text[i]})
    return(hemisphere_image_urls)

#---------------------------------------------------
   

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
