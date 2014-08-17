import requests
import datetime
import re
import json
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
      'message': 'Could not parse row for land, building and contents',
      'exception': e.message,
      'row': row.prettify()
    })

print "%s error(s)" % len(errors)
print json.dumps(assets)
