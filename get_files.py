import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import math
import requests
from bs4 import BeautifulSoup

import csv, urllib2
import shapefile
import os.path
import itertools

def dist(x1, y1, x2, y2):
	return math.sqrt(math.pow(abs(x2-x1),2)+math.pow(abs(y2-y1),2))


base = "https://solweb.tper.it/web/tools/open-data/"
home = requests.get(base + "open-data.aspx?source=tper.it")

home = BeautifulSoup(home.text)

user = "tper_bot"
password = "tperbot123"

to_dl = {
	"Servizio su gomma":{
		"Elenco delle fermate bus":"fermate.csv",
		"Linee bus come sequenza di fermate":"linee_fermate.csv"
	}
}

main_keys = {
	
}

#find files

for row in home.find_all("tr"):
	tds = row.find_all("td")
	try:
		for block in to_dl.keys():
			if tds[1].string == block:
				for dlable in to_dl[block].keys():
					if not os.path.exists(to_dl[block][dlable]):
						if tds[2].string == dlable:
							inner_page = requests.get(base+tds[5].a["href"])
							inner_page = BeautifulSoup(inner_page.text)
							for inner_row in inner_page.find_all("tr"):
								itds = inner_row.find_all("td")
								try:
									if itds[1].span.string == "Formato csv":
										print base+itds[2].a["href"]
										the_file = requests.get(base+itds[2].a["href"])
										print to_dl[block][dlable], "dl-ing"
										with open(to_dl[block][dlable], "wb") as fermate:
											t = the_file.text
											main_keys[to_dl[block][dlable]] = t.split("\n")[0].split(";")
											fermate.write(the_file.content)
										print to_dl[block][dlable], "dl-ed"
								except:
									pass
					else:
						main_keys[to_dl[block][dlable]] = open(to_dl[block][dlable], "rb").read().split("\r\n")[0].split(";")
	except:
		pass

#found files

#clean up files

q_stop = """[out:json];(node[highway=bus_stop](%(bbox)s););out;"""

q_id = """[out:json];(node["highway"="bus_stop"]["ref"="%(ref)s"](%(bbox)s););out;"""

rer = "44.05107684105027,10.84625244140625,44.92786297463683,13.05999755859375" #SONE

url = "http://overpass-api.de/api/interpreter"

param = "data"

radius = 0.00003

#w = shapefile.Writer(shapefile.POINT)
#w.field('codice')
#w.field('denominazione') 
#w.field('ubicazione')
#w.field('comune')

#print "preparing"
#
#with open('fermate.csv', "rb") as csvfile:
#	stop_reader = csv.DictReader(csvfile, delimiter=";")
#	for row in stop_reader:
#			
#		lon = float(row["longitudine"].replace(",","."))
#		lat = float(row["latitudine"].replace(",","."))
#
#		#w.point(lon, lat)
#		#w.record(row["codice"], row["denominazione"], row["ubicazione"], row["comune"])
#w.save('fermate')

full_url = url+"?"+param+"="+q_stop % {"bbox":rer}
print full_url
if not os.path.exists("osm.csv"):
	osm_points = requests.get(full_url)

	keys = [osm_point["tags"].keys() for osm_point in osm_points.json().get("elements")]
	keys.append(["lon","lat", "osm_id"])
	keys = itertools.chain(*keys)
	keys = list(set(keys))


	with open("osm.csv", "wb") as osmfile:
		with open("ids.csv", "wb") as idsfile:
			osmcsv = csv.DictWriter(osmfile, fieldnames=keys)
			osmcsv.writeheader()
			idscsv = csv.writer(idsfile)
			for osm_point in osm_points.json().get("elements"):
				#print osm_point
				op = osm_point["tags"]
				op["lon"] = osm_point["lon"]
				op["lat"] = osm_point["lat"]
				op["osm_id"] = osm_point["id"]
				osmcsv.writerow(op)

				if "ref" in osm_point["tags"]:
					idscsv.writerow([osm_point["tags"]["ref"]])

print main_keys

done_refs = []

osm_list = []
fer_list = []

print "analysis starting"
with open("fermate_importable.csv", "wb") as importables:
	with open("fermate_updatable.csv", "wb") as updatables:
		with open("fermate_manual.csv", "wb") as manually:

			with open("fermate.csv", "rb") as fermate:
				with open("osm.csv", "rb") as osm:	

					fer_csv = csv.DictReader(fermate, delimiter=";")
					osm_csv = csv.DictReader(osm)

					osm_list = [os for os in osm_csv]
					fer_list = [fs for fs in fer_csv]

			imp_csv = csv.DictWriter(importables, fieldnames=main_keys["fermate.csv"])
			upd_csv = csv.DictWriter(updatables, fieldnames = main_keys["fermate.csv"]+["osm_id", "dist"])
			man_csv = csv.DictWriter(manually, fieldnames = main_keys["fermate.csv"])


			imp_csv.writeheader()
			upd_csv.writeheader()
			man_csv.writeheader()

			print "files ready"
			for osm_stop in osm_list:
				for fer_stop in fer_list:
					if not fer_stop["codice"] in done_refs:
						if fer_stop["codice"] == osm_stop["ref"]:
							fer_stop["osm_id"]= osm_stop["osm_id"]
							fer_stop["dist"] = dist(float(osm_stop["lon"]),float(osm_stop["lat"]), float(fer_stop["longitudine"].replace(",",".")), float(fer_stop["latitudine"].replace(",",".")))
							upd_csv.writerow(fer_stop)
							done_refs.append(fer_stop["codice"])
						elif dist(float(osm_stop["lon"]),float(osm_stop["lat"]), float(fer_stop["longitudine"].replace(",",".")), float(fer_stop["latitudine"].replace(",","."))) < radius:
							#print "magic!!!", dist(float(osm_stop["lon"]),float(osm_stop["lat"]), float(fer_stop["longitudine"].replace(",",".")), float(fer_stop["latitudine"].replace(",",".")))
							man_csv.writerow(fer_stop)
							done_refs.append(fer_stop["codice"])
			for fer_stop in fer_list:
				if not fer_stop["codice"] in done_refs:
					imp_csv.writerow(fer_stop)




									
