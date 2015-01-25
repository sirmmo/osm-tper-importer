import csv, urllib2
import requests
import shapefile

q_stop = """[out:json];(node["highway"="bus_stop"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););out;"""

q_id = """[out:json];(node["highway"="bus_stop"]["ref"="%(ref)s"](%(xmin)s,%(ymin)s,%(xmax)s,%(ymax)s););out;"""

EWKT = "SRID=4326;POLYGON ((%(xmin)s %(ymin)s, %(xmin)s %(ymax)s, %(xmax)s %(ymax)s, %(xmax)s %(ymin)s, %(xmin)s %(ymin)s))"

url = "http://overpass-api.de/api/interpreter"

param = "data"

radius = 0.0001

w = shapefile.Writer(shapefile.POINT)
w.field('codice')
w.field('denominazione') 
w.field('ubicazione')
w.field('comune')
with open('fermate.csv') as csvfile:
	stop_reader = csv.DictReader(csvfile, delimiter=";")
	for row in stop_reader:
			
		lon = float(row["longitudine"].replace(",","."))
		lat = float(row["latitudine"].replace(",","."))

		w.point(lon, lat)
		w.record(row["codice"], row["denominazione"], row["ubicazione"], row["comune"])
		q_params = {
			'xmin': lon-radius, 
			'xmax': lon+radius, 
			'ymin': lat-radius,
			'ymax': lat+radius
		}
		q_params["ref"] = row["codice"]

		full_url = url+"?"+param+"="+q_stop % q_params
		print q_params["ref"], full_url, EWKT%q_params

		
		#try:
		#	myUrlHandle = requests.get(full_url)
		#	print myUrlHandle.json()["elements"]
		#except urllib2.URLError as e:
		#	print str(e)

		full_url = url+"?"+param+"="+q_id % q_params


w.save('shapefile')