import threading
from queue import Queue
import os
from crawler import Crawler
from filehandler import *
import time 
import sys 

folder_path = "links"
queue = Queue()
threads_count = 32
threads = list()
lock = threading.Lock()
crawled = set()
event = threading.Event()

if not os.path.exists(folder_path):
    make_directory(folder_path)

if 'crawled.txt' not in os.listdir(folder_path):
    make_file(folder_path, "/crawled.txt")
if ('queued.txt' not in os.listdir(folder_path)) or ('queued.txt' in os.listdir(folder_path) and os.stat(folder_path+"/queued.txt").st_size == 0):
    make_file(folder_path, "queued.txt")
    seed_link = input("Enter the seed link: ")
    Crawler(seed_link, folder_path)
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
    while queue.qsize()>0:
        lock.acquire()
        url = queue.get()
        lock.release()
        print(threading.current_thread().name+" crawling "+url)
        if url not in crawled:
            parsed_links = Crawler.get_links(threading.current_thread().name, url)
            print(threading.current_thread().name+" completed crawling "+url)
            lock.acquire()
            crawled.add(url)
            add_to_queue(parsed_links)
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
        # repeat = threading.Timer(30.0, update_file)
        # repeat.start()
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
        print("No links to write ")

def stop_threads():
    event.set()
    return


write_thread = threading.Thread(target = update_file, args = (event, 30, ))
write_thread.daemon = True
write_thread.start()
file_to_queue()
time.sleep(2)
create_workers()
time.sleep(20)
stop_threads()
update_file(event, time_to_sleep=30)
time.sleep(10)
print("threads stopped")
sys.exit(0)
