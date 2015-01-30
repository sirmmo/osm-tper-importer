import csv


with open("osm_3.csv") as clean:
	with open("ids.csv", "wb") as ids:
		ww = csv.writer(ids)
		for crow in csv.reader(clean):
			ww.writerow([crow[2]])
