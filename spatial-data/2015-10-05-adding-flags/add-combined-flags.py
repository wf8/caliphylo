#! /usr/bin/python
"""
script to add Jepson flags and Maxent modeling indices to combined (GBIF etc) spatial records 
"""

import csv
import codecs
from os import listdir
from os.path import isfile, join

input_dir = ""
output_dir = ""
jepson_dir = "raw_flag_data/yellow_flagging/"
maxent_dir = "raw_flag_data/"
data = ["combined_sources_August_24.csv"]


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

print("Adding flags to combined data...")
id_column = 0
header_row = []
for f in data:
    with open(input_dir + f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
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
