# @author: Bala
# Quick hack, have to include response checks, parsing errors and other run time errors.

import datetime
import urllib2
from dateutil import parser
from bs4 import BeautifulSoup

def save_file(url, name):
  file = urllib2.urlopen(url)
  output = open("downloads/"+name,'wb')
  output.write(file.read())
  output.close()

base_url = "http://www.imd.gov.in/section/dwr/img/"

soup = BeautifulSoup(urllib2.urlopen(base_url).read())

for row in soup('table')[0]('tr')[3:-2]:
  tds = row('td')
  if len(tds) > 0:
    name = tds[1]('a')[0].text
    last_modified = tds[2].text
    last_modified_date = parser.parse(last_modified).date()
    if "_chn" in name and (last_modified_date == datetime.datetime.today().date()):
      print base_url + name + "  --Last Modified-> " + last_modified + "\n"
      url = base_url+name
      save_file(url, name)


