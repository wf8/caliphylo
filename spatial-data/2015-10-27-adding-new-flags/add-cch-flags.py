#! /usr/bin/python
"""
script to add new Jepson flags to spatial records 
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

input_dir = "unflagged/"
output_dir = "flagged/"
jepson_dir = "raw_flag_data/"
id_column = 0
data = [ f for f in listdir(input_dir) if isfile(join(input_dir,f)) ]

#id,star,flag,scientificName,collectors,collectors_parsed,collector_number_prefix,collector_number,collector_number_suffix,early_julian_day,late_julian_day,verbatim_date,county,elevation,locality,locality_parsed,geocoded,longitude,latitude,datum,georeference_source,township_range_section,error_radius,error_radius_units,current_name,current_name_binomial,current_genus,current_species,clade,cloned_geocode


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
#import sys
#sys.exit()

print("Adding flags to spatial data...")
header_row = []
for f in data:
    with open(input_dir + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(csvreader):
            if i == 0:
                header_row = row
            else:
                accession = row[id_column]
                if not isfile(output_dir + f):
                    header_row.append("jepson_flag_october")
                    with open(output_dir + f, "a") as outputfile:
                        csvwriter = csv.writer(outputfile, delimiter=",")
                        csvwriter.writerow(header_row)
                if accession in jepson_flags:
                    row.append("yes")
                else:
                    row.append("no")
                with open(output_dir + f, "a") as outputfile:
                    csvwriter = csv.writer(outputfile, delimiter=",")
                    csvwriter.writerow(row)

print("Done.")
