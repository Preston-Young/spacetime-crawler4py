import re
import requests
from collections import defaultdict

from urllib.parse import urlparse
from bs4 import BeautifulSoup

from stopwords import STOPWORDS_LIST

from urllib.robotparser import RobotFileParser

"""
Report Requirements:
1. Unique pages count: 
    -   Uniqueness for the purposes of this assignment is ONLY established by the URL, 
        but discarding the fragment part.

2. Longest page in terms of the number of words

3. What are the 50 most common words in the entire set of pages crawled under these domains?
    -   Ignore stopwords (stopwords.py)
    -   Submit the list of common words ordered by frequency

4. How many subdomains did you find in the ics.uci.edu domain?
    -   Submit the list of subdomains ordered alphabetically and the number 
        of unique pages detected in each subdomain
"""

unique_pages = set()
longest_page = {"name": "", "length": 0}
word_frequencies = defaultdict(int)
ics_subdomains = defaultdict(int)

# Adds URL to set of unique URLs, ICS Subdomain dictionary
# To be called by scraper after visiting a page
def report_add_url(url):
    global unique_pages
    global ics_subdomains

    unique_pages.add(url)
    
    parsed = urlparse(url)
    if '.ics.uci.edu' in parsed.hostname and 'www' not in parsed.hostname:
        ics_subdomains[f'{parsed.scheme}://{parsed.hostname}'] += 1


#get tokens from url and update word_frequencies/longest_page
def tokenize(url, soup):
    global longest_page
    global word_frequencies
    global STOPWORDS_LIST

    tokens = []
    count = 0
    
    #get tokens
    for token in re.split("[^a-zA-Z']+", soup.get_text().lower()):
        token = token.strip()
        #check for empty token, ascii, and stopwords
        if token != '' and len(token) == len(token.encode()) and token not in STOPWORDS_LIST:
            tokens.append(token)
            count += 1

    #update word counts
    for token in tokens:
        word_frequencies[token] += 1
        
    #check for new longest page
    if count > longest_page["length"]:
        longest_page = {"name": url, "length": count}

def gen_report():
    with open("output.txt", "w") as output:
        output.write(f"1. Number of unique pages: {len(unique_pages)}\n")

        output.write(f"\n2. Longest page:\n")
        output.write(f"{longest_page['name']} -> {longest_page['length']}")
        
        counter = 0
        output.write(f"\n3. 50 most common words:\n")
        for word, freq in sorted(word_frequencies.items(), key = lambda x: -x[1]):
            output.write(f"{word} -> {freq}\n")
            
            counter += 1
            if counter == 50:
                break

        output.write(f"\n4. ics.uci.edu subdomains:\n")
        for subdomain, freq in sorted(ics_subdomains.items()):
            output.write(f"{subdomain} -> {freq}\n")
    
    return