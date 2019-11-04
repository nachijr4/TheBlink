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

    def get_title_for_classifier(self):
        title = self.soup.find("title")
        domain = tldextract.extract(self.current_link)
        return_string = domain.domain+", "+re.sub(r'[^\w]'," ",title.get_text().strip().lower().replace(domain.domain, ""))
        return return_string

    def get_title(self):
        if self.soup.title:
            return self.soup.title.string
        else:
            return None

    def get_article_text(self):
        paragraphs = self.soup.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text

        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        return article_text

    def is_article(self):
        meta_tag = self.soup.find('meta', property = "og:type", content = "article")
        if meta_tag:
            return True
        else:
            return False

    def get_description(self):
        description_tag =  self.soup.find('meta', attrs = {'name' : 'description'})
        try:
            if description_tag:
                return description_tag['content']
            else:
                return None
        except:
            print("Error in description tag", description_tag)

    def get_html_body(self):
        # body = self.soup.find('body')
        # div = body.find_all('div')
        # return "".join(div)
        return self.html
    
    def get_thumbnail(self):
        images = self.soup.find_all('img')
        if len(images)>1:
            for i in images[0].attrs:
                if "src" in i:
                    extentions = [".png",".jpg",".jpeg",".gif",".tiff"]
                    for extention in extentions:
                        if extention in images[0].attrs[i]:
                            isImage = True
                            return images[0].attrs[i]

        return "notfound"

# import requests

# url = "http://www.startribune.com/startribune-com-privacy-policy/218991591/#sharePersonalInfo"
# a = requests.get(url).text

# t = LinkParser(url, a)

# print(t.is_article())
