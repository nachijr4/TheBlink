import threading
from queue import Queue
import os
from crawler import Crawler
from filehandler import *
import time 
import sys
from Database.db import DB

folder_path = "links"
queue = Queue()
threads_count = 16
total_no_of_data_added_to_db = 0
threads = list()
lock = threading.Lock()
crawled = set()
collected_data = []
event = threading.Event()

if not os.path.exists(folder_path):
    make_directory(folder_path)

if 'crawled.txt' not in os.listdir(folder_path):
    make_file(folder_path, "/crawled.txt")
if ('queued.txt' not in os.listdir(folder_path)) or ('queued.txt' in os.listdir(folder_path) and os.stat(folder_path+"/queued.txt").st_size == 0):
    make_file(folder_path, "queued.txt")
    seed_link = input("Enter the seed link: ")
    seed_crawl = Crawler('initial process',seed_link)
    seed_crawl.seed_page(folder_path)
    crawled.add(seed_link)
    print("initial process done")

def file_to_queue():
    lock.acquire()
    for link in read_from_file(folder_path+"/crawled.txt"):
        crawled.add(link)
    for link in read_from_file(folder_path+"/queued.txt"):
        queue.put(link)
    lock.release()
    # queue.join()

def work(event):
    global total_no_of_data_added_to_db
    while queue.qsize()>0:
        lock.acquire()
        url = queue.get()
        lock.release()
        if url not in crawled:
            print(threading.current_thread().name+" crawling "+url)
            crawler = Crawler(threading.current_thread().name, url)
            parsed_links = crawler.get_links()
            print(threading.current_thread().name+" completed crawling "+url)
            lock.acquire()
            crawled.add(url)
            add_to_queue(parsed_links)
            data = crawler.get_data()
            if data != None:
                collected_data.append(crawler.get_data())
                total_no_of_data_added_to_db = 1+total_no_of_data_added_to_db
            if len(collected_data) > 15:
                add_to_database(collected_data)
            lock.release()
        queue.task_done()
        if event.is_set():
            break

def create_workers():
    for _ in range(threads_count):
        t = threading.Thread(target=work, args=(event,))
        t.daemon = True
        threads.append(t)
        t.start()

def update_file(event, time_to_sleep = 20):
    while True:
        lock.acquire()
        if  queue.qsize()>0:
            queue_to_file(folder_path+"/queued.txt", queue)
        if len(crawled):
            write_to_file(folder_path+"/crawled.txt", crawled)
        lock.release()
        time.sleep(time_to_sleep)
        if event.is_set():
            break


def  add_to_queue(links=set()):
    try:
        if len(links) > 0:
            for link in links:
                queue.put(link.strip())
    except:
        print("No links to add ")


def add_to_database(data_to_be_added):
    db = DB()
    if db.insert_many("links", data_to_be_added):
        print("Data stored in database successfully")
    else:
        print("Error in storing data in thedatabase")
    data_to_be_added.clear()

def stop_threads():
    global total_no_of_data_added_to_db
    while total_no_of_data_added_to_db<25:
        continue
    event.set()
    return

write_thread = threading.Thread(target = update_file, args = (event, 60, ))
write_thread.daemon = True
write_thread.start()
print("starting...")
file_to_queue()
time.sleep(2)
create_workers()
time.sleep(300)
stop_threads()
update_file(event, time_to_sleep=60)
time.sleep(10)
add_to_database(collected_data)
print("threads stopped")
sys.exit(0)
