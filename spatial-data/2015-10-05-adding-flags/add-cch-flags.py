#! /usr/bin/python
"""
script to add Jepson flags and Maxent modeling indices to CCH spatial records 
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

input_dir = "spatial_data_unflagged_by_clade/"
output_dir = "spatial_data_flagged/"
jepson_dir = "raw_flag_data/yellow_flagging/"
maxent_dir = "raw_flag_data/"
clade_column = 28
data = [ f for f in listdir(input_dir) if isfile(join(input_dir,f)) ]

#id,star,flag,scientificName,collectors,collectors_parsed,collector_number_prefix,collector_number,collector_number_suffix,early_julian_day,late_julian_day,verbatim_date,county,elevation,locality,locality_parsed,geocoded,longitude,latitude,datum,georeference_source,township_range_section,error_radius,error_radius_units,current_name,current_name_binomial,current_genus,current_species,clade,cloned_geocode

print("Reading maxent data...")
maxent_indices = {}
with open(maxent_dir + "Maxent_outlier_indices.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        maxent_indices[row[1]] = row[3]

print("Reading Jepson flag data...")
jepson_flags = []
jepson_flag_data = [ f for f in listdir(jepson_dir) if isfile(join(jepson_dir,f)) ]
for f in jepson_flag_data:
    with open(jepson_dir + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in csvreader:
            if row[0] not in jepson_flags:
                jepson_flags.append(row[0])

#print len(jepson_flags)
#print len(maxent_indices)
#import sys
#sys.exit()

print("Adding flags to CCH data...")
id_column = 0
header_row = []
for f in data:
    with open(input_dir + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for i, row in enumerate(csvreader):
            if i == 0:
                header_row = row
            else:
                accession = row[id_column]
                if not isfile(output_dir + str(f) + ".csv"):
                    header_row.append("jepson_flag")
                    header_row.append("maxent_index")
                    with open(output_dir + str(f) + ".csv", "a") as outputfile:
                        csvwriter = csv.writer(outputfile, delimiter=",")
                        csvwriter.writerow(header_row)
                if accession in jepson_flags:
                    row.append("yes")
                else:
                    row.append("no")
                try:
                    row.append(maxent_indices[accession])
                except:
                    row.append("NA")
                with open(output_dir + str(f) + ".csv", "a") as outputfile:
                    csvwriter = csv.writer(outputfile, delimiter=",")
                    csvwriter.writerow(row)

print("Done.")
