from html.parser import HTMLParser
from urllib.parse import urljoin

class LinkParser(HTMLParser):

    def __init__(self, current_link):
        super().__init__()
        self.current_parsed_links = set()
        self.current_link  = current_link

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    self.current_parsed_links.add(urljoin(self.current_link, value))

    def get_parsed_links(self):
        return self.current_parsed_links
