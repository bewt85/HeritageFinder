#!/usr/bin/env python

import gevent
from gevent import monkey; monkey.patch_all()

from bottle import route, run, get, post, static_file, request, response, template
import pickle 
import os

assets = []
assets_index = []

def load():
  global assets
  with open("temp_backup.pkl") as backup_file:
    (i, assets, errors) = pickle.load(backup_file)

def index():
  global assets_index
  assetsMap = lambda asset: "{}||{}".format(asset.get('name', ''), asset.get('description', '')).lower()
  assets_index = zip(map(assetsMap, assets), assets)

def filter_assets(search_terms):
  results = assets_index
  for term in search_terms:
    results = filter(lambda asset_string: term in asset_string[0], results)
  return [asset[1] for asset in results]

@get('/')
def search():
  query = request.query.get('q', "")
  content_type = request.get_header('Accept', "")
  if query:
    search_terms = query.lower().split()
    results=filter_assets(search_terms)
  else:
    results=assets
  if content_type.lower() == "application/json":
    return {'count': len(results), 'query': query, 'results': results[:20]}
  else:
    return template('index', count=len(results), query=query, results=results[:20])
  
if __name__ == '__main__':
  load()
  index()
  run(server='gevent', host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
