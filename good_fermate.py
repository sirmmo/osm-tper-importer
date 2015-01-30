import csv


the_ids = []

with open("ids.csv") as ids:
	for ref in csv.reader(ids):
		the_ids.append(ref[0])

print len(the_ids)

the_other_ids = []

with open("osm.csv") as ids:
	for ref in csv.reader(ids, delimiter=";"):
		if ref[3]:
			the_other_ids.append(ref[3])

print len(the_other_ids)

with open("fermate.csv") as fs:
	with open ("fermate_clean.csv", "wb") as cfs:
		cfw = csv.writer(cfs, delimiter=";")
		for fermata in csv.reader(fs, delimiter=";"):
			if fermata[0] in the_ids:
				if fermata[0] not in the_other_ids:
					cfw.writerow(fermata)

