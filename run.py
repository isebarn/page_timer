from selenium import webdriver
import selenium as se
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from urllib.parse import urlparse
import re
import os
from random import choice
from time import time
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
import concurrent.futures
from multiprocessing import Queue
import argparse

queue = Queue()

def client():
  return pymongo.MongoClient(os.environ.get('DATABASE'))

def get_mongo_collection(collection_name):
  database = client()["timer"]
  collection = database[collection_name]

  return collection

def save_root(root):
  root_collection = get_mongo_collection('root')
  root_collection.insert_one(root)

  return root

def save_timings(timings):
  if len(timings) == 0: return None

  timing_collection = get_mongo_collection('timings')
  new_ids = timing_collection.insert_many(timings).inserted_ids

  return new_ids

def run(page):
  try:
    driver = queue.get()

    # fetch the page and time it
    start = time()
    driver.get(page)
    fetch_time = time() - start

    # parse all the timings
    timings = driver.execute_script("return window.performance.getEntries();")

    # save all the timings
    ids = save_timings(timings)

    # save page root entry
    save_root({
      'datetime': datetime.now(),
      'url': page,
      'time': fetch_time,
      'timings': ids
    })
  except Exception as e:
    pass

  queue.put(driver)

def args():
  parser = argparse.ArgumentParser(description='Measure page load times and save to database.')
  parser.add_argument('--cores', default=1, type=int, help='Number of processes')
  parser.add_argument('--sites', default='sites.txt', help='Number of processes')
  return parser.parse_args()

def start_drivers():
  for x in range(0,args.cores):
    capabilities = DesiredCapabilities.FIREFOX
    driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub',
      desired_capabilities=capabilities)

    queue.put(driver)

def load_page_file(filename):
  file = open(filename, "r")
  return file.read().splitlines()

if __name__ == '__main__':
  args = args()
  print("Running with {} cores".format(args.cores))
  pages = load_page_file(args.sites)
  pprint(pages)

  start_drivers()


  e = concurrent.futures.ThreadPoolExecutor(args.cores)
  for x in e.map(run, pages):
    print("Timing saved")

  while queue.qsize() > 0:
    queue.get().close()
