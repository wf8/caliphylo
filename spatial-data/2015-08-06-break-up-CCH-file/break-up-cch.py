#! /usr/bin/python
"""
script to break up the 1910784 CCH records into smaller files organized by genus
"""

import csv
import codecs

org_file = "../org_spatial_data/CCH August 5th 2015/dwca-cch/occurrence.txt"

print("Checking for NULL bytes due to MS Excel...")
fi = open(org_file, 'rb')
data = fi.read()
fi.close()
if data.count('\x00') > 0:
    fo = open(org_file, 'wb')
    fo.write(data.replace('\x00', ''))
    fo.close()


print("Getting the number of records for each genus...")
genera = {}
with open(org_file, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
    for row in csvreader:
        genus = row[24]
        if genus not in genera:
            genera[genus] = 1
        else:
            genera[genus] += 1

print("Allocating genera to output files...")
max_records_per_file = 400000
output_files = [[]]
records_in_file = 0
current_file = 0
for genus in genera.iterkeys():
    if records_in_file + genera[genus] < max_records_per_file:
        output_files[current_file].append(genus)
        records_in_file = records_in_file + genera[genus]
    else:
        current_file += 1
        output_files.append([genus])
        records_in_file = genera[genus]

print("Generating output files...")
with open(org_file, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
    for row in csvreader:
        genus = row[24]
        for i, out in enumerate(output_files):
            if genus in out:
                with open("output/" + str(i) + ".txt", "a") as outputfile:
                    outputfile.write("\t".join(row) + "\n")
                break

print("Done.")
