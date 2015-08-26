#! /usr/bin/python
"""
script to break up the 1798634 CCH records into smaller files organized by county
also needs to add two columns: collector_parse and locality_parsed
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

data = [ f for f in listdir("data/") if isfile(join("data/",f)) ]


print("Getting the number of records for each county...")
counties = {}
header_row = []
for f in data:
    with open("data/" + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(csvreader):
            if i == 0:
                header_row = row
            else:
                county = row[11]
                if county not in counties:
                    counties[county] = 1
                else:
                    counties[county] += 1

print("Allocating counties to output files...")
max_records_per_file = 200000
output_files = [[]]
records_in_file = 0
current_file = 0
for county in counties.iterkeys():
    if records_in_file + counties[county] < max_records_per_file:
        output_files[current_file].append(county)
        records_in_file = records_in_file + counties[county]
    else:
        current_file += 1
        output_files.append([county])
        records_in_file = counties[county]

print("Generating output files...")
for f in data:
    with open("data/" + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(csvreader):
            if i != 0:
                county = row[11]
                for j, out in enumerate(output_files):
                    if county in out:
                        if not isfile("output/" + str(j) + ".txt"):
                            header_row_added = header_row[:5] + ["collectors_parsed"] + header_row[5:14] + ["locality_parsed"] + header_row[14:]
                            with open("output/" + str(j) + ".txt", "a") as outputfile:
                                outputfile.write("\t".join(header_row_added) + "\n")
                        row_added = row[:5] + [""] + row[5:14] + [""] + row[14:]
                        with open("output/" + str(j) + ".txt", "a") as outputfile:
                            outputfile.write("\t".join(row_added) + "\n")
                        break

print("Done.")
