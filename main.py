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

        links.extend(page_links)

    return links[:num_links]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Google search results and extract video links.")
    parser.add_argument("query", help="Query string for Google search")
    parser.add_argument("num_links", type=int, help="Number of links to retrieve")

    args = parser.parse_args()

    scraped_links = scrape_google(args.query, args.num_links)

    # add the video links to a dataframe
    df = pd.DataFrame(scraped_links, columns=['video_link'])

    # export the dataframe to a csv file
    df.to_csv('video_links.csv', index=False)

    channel_links = []
    for link in scraped_links:
        channel_link = get_account_link(link)
        if channel_link:
            channel_links.append(channel_link)
            print(channel_link)

    # add the channel links to a dataframe
    df = pd.DataFrame(channel_links, columns=['channel_link'])

    # export the dataframe to a csv file
    df.to_csv('channel_links.csv', index=False)