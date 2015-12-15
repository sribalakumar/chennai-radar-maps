# @author: Bala
# Quick hack, have to include response checks, parsing errors and other run time errors.
# Ideally save_file and push_to_fb should be synchonous and performed by seperate job via a queue.
# TODO: Save images in a proper folder structure like Month/Date/file_name.
# TODO: proper logging instead of print.
# Script is machine time dependent, should make it independent of system time.

import datetime
import urllib2
import facebook
import time
import os.path
import yaml
from dateutil import parser
from bs4 import BeautifulSoup

#os.environ['TZ'] = "Asia/kolkatta"
#time.tzset()
creds = yaml.load(open(os.path.dirname(os.path.abspath(__file__)) + "/creds.yml"))
en = yaml.load(open(os.path.dirname(os.path.abspath(__file__)) + "/en.yml"))

fb_token = creds['fb_group']['token']

def is_existing_file(file_name, sub_dir):
  directory = directory_path(sub_dir)
  return os.path.isfile(directory + "/" + file_name)

def directory_path(sub_dir):
  return os.path.dirname(os.path.abspath(__file__)) + "/downloads/" + sub_dir

def file_name(lm_date_time, name):
  temp = lm_date_time.timetuple()
  time_stamp = time.mktime(temp)
  return str(time_stamp)[0:-2] + "_" + name

def save_file(url, sub_dir, file_name):
  file = urllib2.urlopen(url)
  directory = directory_path(sub_dir)
  if not os.path.exists(directory):
    os.makedirs(directory)
  output = open(directory + "/" + file_name,'wb')
  output.write(file.read())
  output.close()

def help_text(region):
  return en["help_text"][region]

def post_to_fb(f_name, sub_dir, last_modified):
  graph = facebook.GraphAPI(fb_token)
  required_sub_dir = ["ppi_chn", "caz_chn", "ppz_chn", "sri_chn", "ppz_kkl", "caz_kkl", "sri_kkl"]
  if sub_dir in required_sub_dir:
    path = (directory_path(sub_dir) + "/" + f_name).encode('utf-8')
    with open(path) as image:
      caption = help_text(sub_dir) + " Radar update @ " + last_modified
      image_id = graph.put_photo(image, caption, '')
      print image_id

base_url = "http://www.imd.gov.in/section/dwr/img/"
regions = ["_chn", "_kkl"]

soup = BeautifulSoup(urllib2.urlopen(base_url).read(), "html.parser")

for row in soup('table')[0]('tr')[3:-2]:
  tds = row('td')
  if len(tds) > 0:
    name = tds[1]('a')[0].text
    last_modified = tds[2].text
    lm_date_time = parser.parse(last_modified)
    if any(region in name for region in regions) and (lm_date_time.date() == datetime.datetime.today().date()):
      #print base_url + name + "  --Last Modified-> " + last_modified + "\n"
      url = base_url+name
      sub_dir = name.split(".")[0]
      f_name = file_name(lm_date_time, name)
      if not is_existing_file(f_name, sub_dir):
        try:
          save_file(url, sub_dir, f_name)
          post_to_fb(f_name, sub_dir, last_modified)
        except:
          print "exception with" + f_name + "\n"


