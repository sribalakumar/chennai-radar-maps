import urllib2
import facebook
import yaml
import os.path


creds = yaml.load(open(os.path.dirname(os.path.abspath(__file__)) + "/creds.yml"))
en = yaml.load(open(os.path.dirname(os.path.abspath(__file__)) + "/en.yml"))

fb_token = creds['fb_group']['token']

imd_base_url = "http://www.imd.gov.in/section/dwr/img/"

radar_image_type = ["ppi_chn", "ppz_chn", "sri_chn", "caz_kkl", "ppz_kkl"]

def help_text(region):
  return en["help_text"][region]

def post_to_fb(image):
  graph = facebook.GraphAPI(fb_token)
  #allowed_images = ["ppi_chn", "caz_chn", "ppz_chn", "sri_chn", "ppz_kkl", "caz_kkl", "sri_kkl"]
  allowed_images = ["ppi_chn", "ppz_chn", "sri_chn", "caz_kkl", "ppz_kkl"]
  if image in allowed_images:
    path = ("/home/bala/radar-map-images/"+image+"/"+image+".gif").encode('utf-8')
    with open(path) as photo:
      caption = help_text(image)
      photo_id = graph.put_photo(photo, caption, '')


for image in radar_image_type:
  try:
    file = urllib2.urlopen(imd_base_url + image + ".gif")
    output = open("/home/bala/radar-map-images/"+image+"/"+image+".gif", 'wb')
    output.write(file.read())
    output.close()
    post_to_fb(image)
  except:
    print "exception with " + image





