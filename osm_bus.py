import sys
reload(sys)
sys.setdefaultencoding("utf-8")


import csv, urllib2
import requests
import shapefile
import json

url = "http://overpass-api.de/api/interpreter"

param = "data"



query = """[out:json]
[timeout:25]
;
(
  node
    ["highway"="bus_stop"]
    (44.15068115978091,10.570220947265625,45.02597983843737,12.50244140625);
);
out body;"""



#w = shapefile.Writer(shapefile.POINT)
#w.field('FIRST_FLD')

w = shapefile.Writer(shapefile.POINT)

w.field('lat')
w.field('lon')
w.field('osm_id')
w.field("osm_data", 'C','255 ')

full_url = url+"?"+param+"="+query
print full_url

fields = ["lat", "lon", "osm_id", "osm_data"]

with open('osm.csv', "wb") as csvfile:
	osm_w = csv.writer(csvfile, delimiter=";")

	try:
		myUrlHandle = requests.get(full_url)
		for element in  myUrlHandle.json()["elements"]:
			w.point(element["lon"], element["lat"])
			w.record(element["lat"], element["lon"], element["id"], json.dumps(element["tags"]))
			osm_w.writerow([element["lat"], element["lon"], element["id"], element["tags"].get("name"),element["tags"].get("ref"), element["tags"].get("route_ref"), element["tags"].get("location")])

	except urllib2.URLError as e:
		print str(e)

w.save('osm')


