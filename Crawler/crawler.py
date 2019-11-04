import requests
from link_parser import LinkParser
from filehandler import write_to_file
from Classifier.predictor import Classifier
from Summary.summary import Summary

class Crawler:

    # queued = set()
    # crawled = set()
    queue_path = ''
    crawled_path = ''
    continous_non_article_count = 0

    def __init__(self, process_name, open_url):
        self.html = ""
        self.open_url = open_url
        self.is_html = False
        # self.is_article = False
        try:
            with requests.get(open_url) as response:
                if "text/html" in response.headers['Content-Type']:
                    self.is_html = True
                    self.html = response.text
                    self.parsed_page = LinkParser(open_url, self.html)
                    self.is_article = self.parsed_page.is_article()
                    title_for_crawler = self.parsed_page.get_title_for_classifier()
                    self.classes_of_pages = Classifier.predict([title_for_crawler])[title_for_crawler]
                    self.highest_prob_class = sorted(self.classes_of_pages, key=self.classes_of_pages.get, reverse= True)[0]
                    # self.thumbnails = self.parsed_page.get_thumbnail()
                    if not self.is_article:
                        Crawler.continous_non_article_count +=1
        except:
            print("process " + process_name + " error in reading from URL: " + open_url)
    
    def seed_page(self, folderpath):
        if self.is_html:
            queue_path =folderpath+"/queued.txt"
            queued = self.parsed_page.get_all_links()
            write_to_file(queue_path, queued)

    def get_links(self):
        if self.is_html and self.is_article:
            Crawler.continous_non_article_count = 0
            if self.highest_prob_class == 'Technology':
                queued = self.parsed_page.get_all_links()
                return queued
            else:
                return set()
        else:
            return set()
    
    def get_data(self):
        if self.is_html and self.is_article and self.highest_prob_class == 'Technology':
            return {
                'url' : self.open_url,
                'title' : self.parsed_page.get_title(),
                'thumbnail' : self.parsed_page.get_thumbnail(),
                'description' : self.parsed_page.get_description(),
                # 'html' : self.parsed_page.get_html_body(),
                'content_category' : self.highest_prob_class,
                'page_classes_prob' : self.classes_of_pages,
                'summary' : Summary(self.parsed_page.get_article_text()).get_summary()
            }

# a = Crawler('a',"https://www.washingtonpost.com/politics/2018/12/04/this-watchdog-agency-has-gotten-smaller-quieter-less-active-under-trump/?arc404=true")
# print(a.get_data())