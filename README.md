# SERP-web-crawler
This Python script is a web crawler designed to scrape YouTube channel links from search results. It uses web scraping techniques to fetch the search results for a specific query and extracts the relevant YouTube channel links.

## Using on Google Colab
Provided a Google Colab file which has the same code implemented and doesn't need installation of dependency
```
SERP_YT_LINKSCRAPPER.ipynb
```
## Installation
Provide instructions on how to install and set up your project. Include any dependencies or prerequisites that need to be installed. Step-by-step instructions or commands are helpful here.

```bash
$ git clone https://github.com/Abhijit-Kadalli/SERP-web-crawler.git
$ cd SERP-web-crawler
$ pip install -r requirements.txt
```

Add your Google API key by replacing 'YOUR_API_KEY' in SERP-web-crawler/channel_extracter.py
```python
api_key = 'YOUR_API_KEY'
```
## Usage

query: help="Query string for Google search" <br/>
num_links: type=int, help="Number of links to retrieve"

```bash
python main.py --query <query> --num_links <num_links>
```
