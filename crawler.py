import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os

# Regex pattern to match a url
HTTP_URL_PATTERN = r'^http[s]*://.+'

domain = "openai.com" # <- your domain to be crawled
full_url = "https://openai.com/" # <- your domain to be crawled with http or https

# A Class to parse the html and get the hyperlinks
class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        # a list to store the hyperlinks
        self.hyperlinks = []

    # Override the HTMLParser's handle_starttag method to get the hyperlinks
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        
        # if the tag is an anchor and has the href attribute, add href attr. to list of hyperlinks
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])
    
    # Function to get hyperlinks from url
def get_hyperlinks(url):
        
    # Try to open the url and read the html
    try:
        # Open the url and read the html
        with urllib.request.urlopen(url) as response:

            # If the response is not html, return an empty list
            if not response.info().get('Content-Type').startswith("text/html"):
                return []

            # Decode the html
            html = response.read().decode('utf-8')
    except Exception as e:
        print(e)
        return []

    parser = HyperlinkParser()
    parser.feed(html)

    return  parser.hyperlinks

def get_domain_hyperlinks(local_domain, url):
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None

        # if the link is a url, check if it is within the same domain
        if re.search(HTTP_URL_PATTERN, link):
            # parse the url and check if the domain is the same
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link
        
        # if the link is not a url, check if it is a relative link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"):
                continue
            clean_link = "https://" + local_domain + "/" + link
            
        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    # return the list of hyperlinks that are within the same domain
    return list(set(clean_links))

def crawl(url):
    # parse the url and get the domain
    local_domain = urlparse(url).netloc

    # create a queue to store the urls to crawl
    queue = deque([url])

    # create a set to store the urls that have already been crawled
    seen = set([url])

    # create a directory to store the text files
    if not os.path.exists("text/"):
        os.mkdir("text/")

    if not os.path.exists(f"text/{local_domain}/"):
        os.mkdir(f"text/{local_domain}/")

    # create a directory to store the csv files
    if not os.path.exists("processed"):
        os.mkdir("processed")

    # while the queue is not empty, continue crawling
    while queue:
        
        # get the next url from the queue
        url = queue.pop()
        print(url) # for debugging and to see the progress

        # save text from the url to a <url>.txt file
        with open("text/" + local_domain + "/" + url[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:
            
            # get the text from the url using beautifulsoup
            soup = BeautifulSoup(requests.get(url).text, "html.parser")

            # get the text but remove the tags
            text = soup.get_text()

            # if the crawler gets to a page that requires js, it will stop the crawl
            if ("You need to enable JavaScript to run this app." in text):
                print("Unable to parse page " + url + " due to JavaScript being required")

            # otherwise, write the text to the file in the text dir
            f.write(text)

        # get the hyperlinks from the url and add them to the queue
        for link in get_domain_hyperlinks(local_domain, url):
            if link not in seen:
                queue.append(link)
                seen.add(link)

crawl(full_url)
