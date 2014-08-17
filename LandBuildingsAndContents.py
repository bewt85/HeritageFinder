import requests
import datetime
import re
import json
import time
from bs4 import BeautifulSoup

SEARCH_URL = "http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoLandDbQueryServlet?region=0&colflag=N"
domain = '/'.join(SEARCH_URL.split('/')[:3])

r = requests.get(SEARCH_URL)
soup = BeautifulSoup(r.text)

biggest_table = max(soup.find_all('table'), key=len)
assets = []
errors = []
now = datetime.datetime.now().isoformat()
for row in biggest_table.find_all('tr')[1:]:
  try:
    field = row.find_all('td')
    relative_url = field[0].a['href']
    full_url = domain + relative_url
    # e.g. '/servlet/com.eds.ir.cto.servlet.CtoLandDetailServlet?ID=313'
    asset_id = re.match(".*[?&]ID=(\d+).*", relative_url).group(1)
    asset_name = field[1].b.text.strip()
    region = field[2].text.strip()
    assets.append({
      'asset_id': asset_id,
      'type': "land, building and contents",
      'name': asset_name,
      'region': region,
      'updated': now,
      'url': full_url
    })
  except Exception as e:
    errors.append({
      'message': 'Could not parse summary row for land, building and contents',
      'exception': e.message,
      'row': row.prettify()
    })

for asset in assets:
  time.sleep(1)
  print ".", 
  try:
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
    asset['description'] = details.get('description', "")
    asset['fax'] = details.get('fax number', "")
    asset['country'] = details.get('country', "")
    asset['email'] = details.get('email', "")
    asset['os_grid_ref'] = details.get('os grid ref', "")
    asset['contact_name'] = details.get('contact name', "")
    asset['access_details'] = details.get('access details', "")
    asset['telephone'] = details.get('telephone no', "")
  except Exception as e:
    errors.append({
      'message': 'Could not parse details for land, building and contents',
      'exception': e.message,
      'row': asset['url'] 
    })
    assets.remove(asset)

print "%s error(s)" % len(errors)
#print json.dumps(assets)
