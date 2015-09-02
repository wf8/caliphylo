#! /usr/bin/python
"""
script to clean locality:
    - read in Locality_abreviations.csv
    - each row is abbreviation,replacement
    - replace each abbreviation is 3 forms:
        - _abbreviation_
        - when string begins with abbreviation_
        - when string end with _abbreviation
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

# column indexes
locality_index = 14
locality_parsed_index = 15
locality_other_source_index = 35

data = [ f for f in listdir("input/") if isfile(join("input/",f)) ]

print("Reading in Locality_abreviations.csv...")
abbreviations = {}
with open("Locality_abreviations.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        abbreviations[row[0]] = row[1]

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def scrub(locality):
    locality = locality.replace("&iacute;", "'")
    locality = locality.replace("&IACUTE;","'")
    for key, value in abbreviations.iteritems():
        if " " + key + " " in locality:
            locality = locality.replace(" " + key + " ", " " + value + " ")
        if key + " " in locality and locality.startswith(key + " "):
            locality = locality.replace(key + " ", value + " ", 1)
        if " " + key in locality and locality.endswith(" " + key):
            locality = rreplace(locality, " " + key, " " + value, 1)
    return locality

for data_file in data:
    print("Reading in " + data_file + "...")
    complete_records = []
    num_records = 0
    with open("input/" + data_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            if num_records != 0:
                if data_file == "combined_sources_August_24.csv":
                    locality = row[locality_other_source_index]
                else:
                    locality = row[locality_index]

                locality = scrub(locality)

                if data_file == "combined_sources_August_24.csv":
                    row.append(locality)
                else:
                    row[locality_parsed_index] = locality
            with open("output/" + data_file + ".txt", "a") as outputfile:
                outputfile.write("\t".join(row) + "\n")
            num_records += 1
print("Done.")
