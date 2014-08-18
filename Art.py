import requests
import datetime
import re
import json
import time
import pickle
from bs4 import BeautifulSoup

SEARCH_URL = "http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDbQueryServlet?location=All&class1=All&freetext=&Submit=search"
domain = '/'.join(SEARCH_URL.split('/')[:3])

def getAssetSummaries():
  summary_page = requests.get(SEARCH_URL)
  soup = BeautifulSoup(summary_page.text)
  hasFourColumns = lambda row: len(row.find_all('td')) == 4
  rows = filter(hasFourColumns, soup.find_all('tr'))
  assets = []
  errors = []
  now = datetime.datetime.now().isoformat()
  for row in rows: 
    try:
      field = row.find_all('td')
      relative_url = field[0].a['href']
      full_url = domain + relative_url
      # e.g. 'http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDetailServlet?ID=34945'
      asset_id = re.match(".*[?&]ID=(\d+).*", relative_url).group(1)
      asset_name = field[1].b.text.strip()
      region = field[2].text.strip()
      category = field[3].text.strip()
      assets.append({
        'asset_id': asset_id,
        'type': "art",
        'category': category,
        'name': asset_name,
        'region': region,
        'updated': now,
        'url': full_url
      })
    except Exception as e:
      errors.append({
        'message': 'Could not parse summary row for art',
        'exception': e.message,
        'row': row.prettify()
      })
  return (assets, errors)

def updateAssetDetails(asset):
  details_url = asset['url']
  details_page = requests.get(details_url)
  details_soup = BeautifulSoup(details_page.text)
  details_table = max(details_soup.find_all('table'), key=len)
  details = {}
  key = ""
  for row in details_table.find_all('tr'):
    (rough_key, value) = map(lambda el: el.text.strip(), row.find_all('td')[1:3])
    if "The Inland Revenue is not responsible for" in value:
      break
    if rough_key == "" and key == "web site(s)":
      # i.e. the previous line was a website, this probably is too
      asset['websites'].append(value)
    key = rough_key.split(':')[0].lower()
    if key == "web site(s)":
      asset.setdefault('websites', []).append(value)
    else:
      details[key] = value
  asset['contact_address'] = details.get('contact address', "")
  asset['contact_reference'] = details.get('contact reference', "")
  asset['description'] = details.get('description', "")
  asset['fax'] = details.get('fax number', "")
  asset['email'] = details.get('email', "")
  asset['contact_name'] = details.get('contact name', "")
  asset['access_details'] = details.get('access details', "")
  asset['telephone'] = details.get('telephone no', "")

  links = details_soup.find_all('a')
  undertakings_links = [link['href'] for link in links if link.text == "Undertakings"]
  if len(undertakings_links) == 1:
    asset['undertakings'] = domain + undertakings_links[0]

if __name__ == "__main__":
  (assets, errors) = getAssetSummaries()
  with open("art_original_backup.pkl", "w") as backup_file:
    pickle.dump((0, assets, errors), backup_file)
  for (i, asset) in enumerate(assets):
    if i % 60 == 0:
      print "%s percent complete" % (100.0 * float(i) / len(assets))
      with open("art_running_backup.pkl", "w") as backup_file:
        pickle.dump((i, assets, errors), backup_file)
    time.sleep(1)
    try:
      updateAssetDetails(asset)
    except Exception as e:
      errors.append({
        'message': 'Could not parse details for art',
        'exception': e.message,
        'row': asset['url'] 
      })
      assets.remove(asset)

  with open("art_final_backup.pkl", "w") as backup_file:
    pickle.dump((i, assets, errors), backup_file)

  print "%s error(s)" % len(errors)
  with open("art_assets.json", "w") as assets_file:
    assets_file.write(json.dumps(assets, sort_keys=True, indent=2, separators=(",", ": ")))

  with open("art_errors.json", "w") as errors_file:
    errors_file.write(json.dumps(errors, sort_keys=True, indent=2, separators=(",", ": ")))
