#! /usr/bin/python
"""
script to break up dataset into smaller files organized by clade
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

input_dir = "input/"
output_dir = "output/"
clade_column = 29
max_records_per_file = 460000
data = [ f for f in listdir(input_dir) if isfile(join(input_dir,f)) ]

print("Getting the number of records for each clade...")
clades = {}
header_row = []
for f in data:
    with open(input_dir + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(csvreader):
            if i == 0:
                header_row = row
            else:
                clade = row[clade_column]
                if clade not in clades:
                    clades[clade] = 1
                else:
                    clades[clade] += 1

print("Allocating clades to output files...")
output_files = [[]]
records_in_file = 0
current_file = 0
for clade in clades.iterkeys():
    if records_in_file + clades[clade] < max_records_per_file:
        output_files[current_file].append(clade)
        records_in_file = records_in_file + clades[clade]
    else:
        current_file += 1
        output_files.append([clade])
        records_in_file = clades[clade]

print("Generating output files...")
for f in data:
    with open(input_dir + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(csvreader):
            if i != 0:
                clade = row[clade_column]
                for j, out in enumerate(output_files):
                    if clade in out:
                        if not isfile(output_dir + "Spatial_Data_" + str(j + 1) + ".csv"):
                            with open(output_dir + "Spatial_Data_" + str(j + 1) + ".csv", "a") as outputfile:
                                csvwriter = csv.writer(outputfile, delimiter=",")
                                csvwriter.writerow(header_row)
                        with open(output_dir + "Spatial_Data_" + str(j + 1) + ".csv", "a") as outputfile:
                            csvwriter = csv.writer(outputfile, delimiter=",")
                            csvwriter.writerow(row)
                        break

print("Done.")
