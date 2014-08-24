#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

from bottle import route, run, get, post, static_file, request, response, template, default_app 
import json 
import os
import requests
import datetime
import math
import re

assets = []
assets_index = []
categories = []

asset_dowload_root = os.environ.get('DOWNLOAD_ROOT', 'https://raw.githubusercontent.com/bewt85/HeritageFinder/master/')
asset_filenames = ['data/art_assets.json', 'data/art_collection_assets.json', 'data/LBC_assets.json']

SUMMARY_LENGTH=140

load_errors = []
load_time = ""

app = default_app()

def load():
  global assets
  global load_errors
  global load_time
  assets = []
  load_errors = []
  print "Loading data from %s" % asset_dowload_root
  print "Set the DOWNLOAD_ROOT environment variable if you want data from somewhere else"
  for asset_filename in asset_filenames:
    try:
      response = requests.get(asset_dowload_root + asset_filename)
      assets += response.json()
    except ValueError:
      load_errors.append("Could not load '%s' from '%s'" % (asset_filename, asset_download_root))
  load_time = datetime.datetime.now().isoformat()

  for asset in assets:
    asset.setdefault('category', asset['type'])
    summary = asset['name']
    if len(summary) > SUMMARY_LENGTH:
      summary = summary[:SUMMARY_LENGTH-3] + "..."
    asset.setdefault('summary', summary) 

def index():
  global assets_index
  assets_index = []
  for asset in assets:
    search_index = "||".join([
      asset.get('name', ''),
      asset.get('description', ''),
      asset.get('category', ''),
      asset.get('location', '')
    ]).lower()
    assets_index.append((search_index, asset))

def createCategories():
  global categories
  getCategory = lambda asset: asset.get('category', '').title()
  categories = map(getCategory, assets)
  deduplicate = lambda l: list(set(l))
  categories = deduplicate(categories)
  categories = sorted(categories)
  categoryAlphaPairs = lambda category: (category, re.sub(r'[^a-zA-Z]', '', category))
  categories = map(categoryAlphaPairs, categories)

def filter_assets(search_terms):
  results = assets_index
  for term in search_terms:
    results = filter(lambda asset_string: term in asset_string[0], results)
  return [asset[1] for asset in results]

def paginate(results, query, page, results_per_page=20):
  number_of_pages = int(math.ceil(float(len(results))/results_per_page))
  
  pageInRange = lambda p: p >= 1 and p <= number_of_pages

  pages_to_show = [1, number_of_pages] + range(page-2,page+3)
  pages_to_show = filter(pageInRange, pages_to_show)
  pages_to_show = sorted(list(set(pages_to_show)))

  toLink = lambda p: (p, app.get_url('root', q=query, p=p))
  links = map(toLink, pages_to_show)
  
  page_start = results_per_page * (page - 1)
  these_results = results[page_start:(page_start+results_per_page)]
  count = len(results)
  
  return {
    'count': count, 
    'query': query, 
    'results': these_results, 
    'page': page, 
    'number_of_pages': number_of_pages, 
    'results_per_page': results_per_page, 
    'links': links}

def search(query="", page=1):
  if query:
    search_terms = query.lower().split()
    results=filter_assets(search_terms)
  else:
    results=assets
  return paginate(results, query, page)

@app.get('/', name='root')
def root():
  query = request.GET.get('q', "")
  page = int(request.GET.get('p', 1))
  requested_categories = request.GET.getall('cat')
  content_type = request.get_header('Accept', "")
  response = search(query, page)  
  if content_type.lower() == "application/json":
    return response 
  else:
    return template('index', categories=categories, requested_categories=requested_categories, **response) 

@app.get("/results")
def results():
  query = request.GET.get('q', "")
  page = int(request.GET.get('p', 1))
  requested_categories = request.GET.getall('cat')
  content_type = request.get_header('Accept', "")
  response = search(query, page)  
  if content_type.lower() == "application/json":
    return response 
  else:
    return template('results', **response) 

@app.get('/status')
def status():
  status = 'red' if load_errors else 'green'
  return { 'status': status, 'errors': load_errors, 'last_loaded': load_time, 'source': asset_dowload_root }

if __name__ == '__main__':
  load()
  index()
  createCategories()
  run(server='gevent', host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
