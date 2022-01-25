import re
import requests as rq

from utils.response import Response
from configparser import ConfigParser
from utils.config import Config
from urllib.parse import urlparse
from utils.download import download

from bs4 import BeautifulSoup
import cbor

url_set = set()
valid_hostnames = [
    '.ics.uci.edu',
    '.cs.uci.edu',
    '.informatics.uci.edu',
    '.stat.uci.edu',
    '.today.uci.edu/department/information_computer_sciences'
]

def scraper(url, resp):
    url_set.add(url)
    links = extract_next_links(url, resp)
    return links

#TODO
# url: the URL that was used to get the page
# resp.url: the actual url of the page
# resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
# resp.error: when status is not 200, you can check the error here, if needed.
# resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
#         resp.raw_response.url: the url, again
#         resp.raw_response.content: the content of the page!
# Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
def extract_next_links(url, resp):
    # TODO: Do error checking for statuses that aren't 200

    if resp.status != 200:
        return
    
    soup = BeautifulSoup(resp.raw_response.content, 'lxml')

    links = []
    for link in soup.find_all('a'):
        link = link.get('href').split('#', 1)[0] # Extract fragments

        if is_valid(link) and link not in url_set:
            links.append(link)
            url_set.add(link)

    return links

# Decide whether to crawl this url or not. 
# If you decide to crawl it, return True; otherwise return False.
# There are already some conditions that return False.
def is_valid(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        
        return parsed.scheme in set(["http", "https"]) and any(h in hostname for h in valid_hostnames)

    except TypeError:
        print ("TypeError for ", parsed)
        raise

if __name__ == "__main__":
    cparser = ConfigParser()
    cparser.read('config.ini')
    config = Config(cparser)
    url = 'https://www.ics.uci.edu/~eppstein/163/'
    resp = rq.get(
        url,
        params=[("q", f"{url}"), ("u", f"{config.user_agent}")]
    )

    print(resp,end='\n\n')

    try:
        if resp and resp.content:
            # print(resp.content) # Prints HTML of page
            # print(cbor.loads(resp.content))
            # print(Response(cbor.loads(resp.content)))
            # print(scraper(url,Response(cbor.loads(resp.content))))
            print(download(url, download(url, config)))
            # print(scraper(url, download(url, config)))
    except (EOFError, ValueError) as e:
        pass