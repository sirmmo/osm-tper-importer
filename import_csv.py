import csv

from osmapi import OsmApi
MyApi = OsmApi(username="sirmmo", password="cip50z321")
MyApi.ChangesetCreate({u"comment": u"Castel M1aggiore Bus stop cleanup"})

with open("CM.csv") as cm_file:
	for row in csv.reader(cm_file, delimiter=";"):
		to_push = {"lon":row[7].replace(",","."), "lat":row[6].replace(",","."), "tag":{"addr:city":row[3].title(), "highway":"bus_stop", "ref":row[0], "name":row[1].title(), "operator":"TPER", "source": "http://www.tper.it/azienda/tper-open-data"}}
		print to_push
		MyApi.NodeCreate(to_push)

MyApi.ChangesetClose()
