from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tldextract import tldextract
import re

class LinkParser():

    def __init__(self, current_link, html):
        self.current_parsed_links = set()
        self.current_link  = current_link
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_all_links(self):
        for link in self.soup.find_all('a'):
            self.current_parsed_links.add(urljoin(self.current_link, link.get('href')))
        return self.current_parsed_links

    def get_title(self):
        title = self.soup.find("title")
        domain = tldextract.extract(self.current_link)
        return domain.domain+", "+re.sub(r'[^\w]'," ",title.get_text().strip().lower().replace(domain.domain, ""))


# import requests

# a = requests.get("https://medium.com/@factoryhr/elasticsearch-introduction-implementation-and-example-17dd66c35c35").text

# t = LinkParser("https://medium.com/@factoryhr/elasticsearch-introduction-implementation-and-example-17dd66c35c35", a)

# print(t.get_title())
