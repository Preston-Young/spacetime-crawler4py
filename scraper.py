import re
from urllib.parse import urlparse, urldefrag, urljoin

from bs4 import BeautifulSoup

from report_helper import report_add_url, tokenize, gen_report
from robot_helper import robot_check

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
    # print(links)
    gen_report()
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
    # Maybe add a checksum for Extra Credit pt2, webpage similarity detection
    #

    links = []

    if resp.status != 200:
        return links
    
    soup = BeautifulSoup(resp.raw_response.content, 'lxml')
    num_atag = len(soup.find_all('a'))
    num_text = len(soup.get_text().split())

    for link in soup.find_all('a'):
        if not link or not link.get('href'):
            continue

        link = urldefrag(link.get('href'))[0] # Extract fragments

        if is_valid(link, num_atag, num_text) and link not in url_set:
            links.append(link)
            url_set.add(link)

            #tokenize the text for each link
            tokenize(url, soup)

            # Add to report info
            report_add_url(link)

    return links


#We need to check whether or not the url is a trap of some sort
def is_trap(url, parsed, num_atag, num_text):

    # check arbit length of url h
    if len(url) > 100:  
        return False

    # TODO
    # Calendar is not accurately being filtered out
    if re.match(r"^.*calendar.*$", parsed.path.lower()):
        return True
        
    # archives are also a trap
    if re.match(r"^archive.*", parsed.path.lower()):
        return True

    # check repeated directories
    #if re.match(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed.path.lower()):
        #return True

    return num_atag / num_text > 0.3 

# Decide whether to crawl this url or not. 
# If you decide to crawl it, return True; otherwise return False.
# There are already some conditions that return False.
def is_valid(url, num_atag, num_text):
    try:
        parsed = urlparse(url)
        
        # Scheme must be HTTP/HTTPS
        if parsed.scheme not in set(["http", "https"]):
            return False
    
        hostname = parsed.hostname
        
        # Hostname not present or Invalid hostname
        if not hostname or not any(h in hostname for h in valid_hostnames):
            return False
        
        # Is a trap link
        if is_trap(url, parsed, num_atag, num_text) and robot_check(parsed):
            return False

        # if file extension is in the path
        return not re.match(   
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ppsx|ppt"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
