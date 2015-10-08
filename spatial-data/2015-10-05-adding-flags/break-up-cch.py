#! /usr/bin/python
"""
script to break up CCH into smaller files organized by clade
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

input_dir = "spatial_data_unflagged_by_county/"
output_dir = "spatial_data_unflagged_by_clade/"
clade_column = 28
data = [ f for f in listdir(input_dir) if isfile(join(input_dir,f)) ]

#id,star,flag,scientificName,collectors,collectors_parsed,collector_number_prefix,collector_number,collector_number_suffix,early_julian_day,late_julian_day,verbatim_date,county,elevation,locality,locality_parsed,geocoded,longitude,latitude,datum,georeference_source,township_range_section,error_radius,error_radius_units,current_name,current_name_binomial,current_genus,current_species,clade,cloned_geocode

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
                if len(row) != 30:
                    print f
                    print row
                clade = row[clade_column]
                if clade not in clades:
                    clades[clade] = 1
                else:
                    clades[clade] += 1

print("Allocating clades to output files...")
max_records_per_file = 200000
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
                        if not isfile(output_dir + str(j) + ".txt"):
                            with open(output_dir + str(j) + ".txt", "a") as outputfile:
                                outputfile.write("\t".join(header_row) + "\n")
                        with open(output_dir + str(j) + ".txt", "a") as outputfile:
                            outputfile.write("\t".join(row) + "\n")
                        break

print("Done.")
