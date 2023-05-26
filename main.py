import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import argparse

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
    account_link = []
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
                account_link.append(get_account_link(url))

        links.extend(page_links)

    return links[:num_links], account_link

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Google search results and extract video links.")
    parser.add_argument("query", help="Query string for Google search")
    parser.add_argument("num_links", type=int, help="Number of links to retrieve")

    args = parser.parse_args()

    scraped_links, scraped_account_links = scrape_google(args.query, args.num_links)

    # add the video links to a dataframe
    df = pd.DataFrame(scraped_links, columns=['video_link'])

    # export the dataframe to a csv file
    df.to_csv('data/video_links.csv', index=False)

    # add the channel links to a dataframe
    df = pd.DataFrame(scraped_account_links, columns=['channel_link'])

    # export the dataframe to a csv file
    df.to_csv('data/channel_links.csv', index=False)