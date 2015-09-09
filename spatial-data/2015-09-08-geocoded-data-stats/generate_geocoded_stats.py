#! /usr/bin/python
"""
computes % geocoded total and in each county for each clade, genera, and species
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

org_files = [ f for f in listdir("../2015-09-07-clone-CCH-geocodes/output/") if isfile(join("../2015-09-07-clone-CCH-geocodes/output/",f)) ]

# column indexes
lon = 17
#lat = 18
#locality = 15
#collector = 5
#date = 10
#datum = 19
#error_radius = 22
#error_units = 23
#accession = 0
#georeference_source = 20
binomial_row = 25
county_row = 12
clade_row = 28

def get_genus(row):
    binomial = row[binomial_row]
    names = binomial.split(' ')
    return names[0]


def get_species(row):
    binomial = row[binomial_row]
    names = binomial.split(' ')
    return names[1]


def get_accepted_binomial(row):
    binomial = row[binomial_row].strip()
    if " " in binomial:
        binomial = binomial.replace(" ", "_")
    return binomial


class Taxon:

    def __init__(self):
        self.total_records = 0
        self.geocoded_records = 0
        self.counties = []
        self.counties_total_records = []
        self.counties_geocoded_records = []

    def update(self, row):
        self.total_records += 1
        geocoded = False
        if row[lon].strip() != "":
            geocoded = True
            self.geocoded_records += 1
        county = row[county_row]
        if county in self.counties:
            c = self.counties.index(county)
            self.counties_total_records[c] += 1
            if geocoded:
                self.counties_geocoded_records[c] += 1
        else:
            self.counties.append(county)
            self.counties_total_records.append(0)
            self.counties_geocoded_records.append(0)
            c = self.counties.index(county)
            self.counties_total_records[c] += 1
            if geocoded:
                self.counties_geocoded_records[c] += 1

    def get_percent_geocoded_total(self):
        if self.total_records == 0:
            return 0.0
        else:
            return round(self.geocoded_records/float(self.total_records), 2)

    def get_percent_geocoded_by_county(self, county):
        if county in self.counties:
            c = self.counties.index(county)
            if self.counties_total_records[c] == 0:
                return 0.0
            else:
                return round(self.counties_geocoded_records[c]/float(self.counties_total_records[c]), 2)
        else:
            return 0.0


print("Getting list of all clades, genera, and species...")
clades = {}
genera = {}
species = {}
with open("../org_spatial_data/Californian_Clade_Masterlist.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_NONE)
    for row in csvreader:
        if row[1] not in clades:
            clades[row[1]] = Taxon()
        if row[0] not in species:
            species[row[0]] = Taxon()
        names = row[0].split("_")
        if names[0] not in genera:
            genera[names[0]] = Taxon()
clades["unplaced"] = Taxon()

all_counties = []
print("Counting geocoded records for all taxa...")
for rfile in org_files:
    with open("../2015-09-07-clone-CCH-geocodes/output/" + rfile, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for i, row in enumerate(csvreader):
            if i != 0:
                if row[county_row] not in all_counties:
                    all_counties.append(row[county_row])
                clades[row[clade_row]].update(row)
                if row[clade_row] != "unplaced":
                    genera[get_genus(row)].update(row)
                    binomial = get_accepted_binomial(row)
                    if binomial in species:
                        species[binomial].update(row)
all_counties.sort()
            

print("Generating output files...")
header = ["taxon", "total number of records", "% total geocoded"]
for county in all_counties:
    header.append(county)
with open("clades.txt", "a") as outputfile:
    outputfile.write("\t".join(header) + "\n")
with open("genera.txt", "a") as outputfile:
    outputfile.write("\t".join(header) + "\n")
with open("species.txt", "a") as outputfile:
    outputfile.write("\t".join(header) + "\n")

for key in clades:
    results = [key, str(clades[key].total_records), str(clades[key].get_percent_geocoded_total())]
    for county in all_counties:
        results.append(str(clades[key].get_percent_geocoded_by_county(county)))
    with open("clades.txt", "a") as outputfile:
        outputfile.write("\t".join(results) + "\n")

for key in genera:
    results = [key, str(genera[key].total_records), str(genera[key].get_percent_geocoded_total())]
    for county in all_counties:
        results.append(str(genera[key].get_percent_geocoded_by_county(county)))
    with open("genera.txt", "a") as outputfile:
        outputfile.write("\t".join(results) + "\n")

for key in species:
    results = [key, str(species[key].total_records), str(species[key].get_percent_geocoded_total())]
    for county in all_counties:
        results.append(str(species[key].get_percent_geocoded_by_county(county)))
    with open("species.txt", "a") as outputfile:
        outputfile.write("\t".join(results) + "\n")

print("Done.")
