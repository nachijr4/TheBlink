import requests
from link_parser import LinkParser
from filehandler import write_to_file
from Classifier.query_testing import Classifier

class Crawler:

    # queued = set()
    # crawled = set()
    queue_path = ''
    crawled_path = ''

    def __init__(self,open_url, folderpath):
        Crawler.open_url = open_url
        Crawler.queue_path =folderpath+"/queued.txt"
        Crawler.crawled_path =folderpath+"/crawled.txt"
        Crawler.get_links( "Initial Process", Crawler.open_url, 1)

    @staticmethod
    def get_links(process_name, url, write = 0):
        html = ''
        try:
            with requests.get(url) as response:
                if "text/html" in response.headers['Content-Type']:
                    html = response.text
                    parsed_page = LinkParser(url, html)
                    title_for_crawler = parsed_page.get_title_for_classifier()
                    #  Probabilities of the pages is found by the classifier
                    classes_of_pages = Classifier.predict([title_for_crawler])[title_for_crawler]
                    if sorted(classes_of_pages, key=classes_of_pages.get, reverse= True)[0] == 'Technology':
                        queued = parsed_page.get_all_links()
                        if write is 1:
                            write_to_file(Crawler.queue_path, queued)
                        else:
                            return queued
                    else:
                        return ()
        except:
            print("process " + process_name + " error in reading from URL: " + url)
            if write is 0:
                return set()