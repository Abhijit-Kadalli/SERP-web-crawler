
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

from channel_extracter import *

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query,num_links):
    query = urllib.parse.quote_plus(query)
    links = []
    #num_links = 1000  # Number of links to retrieve
    num_results_per_page = 10  # Number of results per page

    while len(links) < num_links:
        page_num = len(links) // num_results_per_page + 1
        start_num = len(links) % num_results_per_page

        response = get_source("https://www.google.com/search?q={}&start={}".format(query, start_num))
        page_links = list(response.html.absolute_links)

        google_domains = (
            'https://www.google.',
            'https://google.',
            'https://webcache.googleusercontent.',
            'http://webcache.googleusercontent.',
            'https://policies.google.',
            'https://support.google.',
            'https://maps.google.'
        )

        for url in page_links[:]:
            if url.startswith(google_domains):
                page_links.remove(url)
            else:
                url = get_account_link(url)

        links.extend(page_links)

    return links[:num_links]

scraped_links = scrape_google("site:youtube.com openinapp.co",1000)


# Create a Pandas dataframe from the scraped links
df = pd.DataFrame({'link': scraped_links})

# Export the dataframe to a CSV file
df.to_csv('scraped_links.csv', index=False)