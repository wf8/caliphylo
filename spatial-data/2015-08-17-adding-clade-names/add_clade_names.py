#! /usr/bin/python
"""
script to add clades name from the Californian_Clade_Masterlist to the spatial data
script must also merge the CCH_Erythranthe_clipped.txt into CCH_Native_Plants_Part_2.csv
"""

import csv
import codecs

org_files = ["../org_spatial_data/CCH August 16th 2015/CCH_Native_Plants_Part_1.csv","../org_spatial_data/CCH August 16th 2015/CCH_Native_Plants_Part_2.csv",
            "../org_spatial_data/CCH August 16th 2015/CCH_Native_Plants_Part_3.csv","../org_spatial_data/CCH August 16th 2015/CCH_Native_Plants_Part_4.csv"]

print("Appending CCH_Erythranthe_clipped.txt to CCH_Native_Plants_Part_2.csv...")
with open("../org_spatial_data/CCH August 16th 2015/CCH_Erythranthe_clipped.txt", 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
    for row in csvreader:
        newrow = []
        for i, column in enumerate(row):
            if i == 1:
                newrow.append("")
                newrow.append("")
            if i == 12:
                if row[12].strip() != "":
                    newrow.append("yes")
                else:
                    newrow.append("")
            if "," in column:
                newrow.append('"' + column + '"')
            else:
                newrow.append(column)
        with open("../org_spatial_data/CCH August 16th 2015/CCH_Native_Plants_Part_2.csv", "a") as outputfile:
            outputfile.write(",".join(newrow) + "\n")

print("Reading Californian_Clade_Masterlist.csv...")
clades_dict = {}
clades = []
with open("../org_spatial_data/Californian_Clade_Masterlist.csv", 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_NONE)
    for row in csvreader:
        clades_dict[row[0]] = row[1]
        if row[1] not in clades:
            clades.append(row[1])

for i, rfile in enumerate(org_files):
    print("Adding clade name to records in file " + str(i) + ".txt...")
    total = 0
    not_found = 0
    with open(rfile, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            total += 1
            accepted = row[23].replace(" ", "_")
            if accepted in clades_dict:
                row.append(clades_dict[accepted])
                with open("output/" + str(i) + ".txt", "a") as outputfile:
                    outputfile.write("\t".join(row) + "\n")
            else:
                # these are most specimens ID'd only to genus, so check if we can place them in a clade
                if accepted in clades:
                    row.append(accepted)
                    with open("output/" + str(i) + ".txt", "a") as outputfile:
                        outputfile.write("\t".join(row) + "\n")
                else:
                    # check if we have a header row
                    if "current_name_binomial" in accepted:
                        row.append("clade")
                    else:
                        row.append("?")
                    with open("output/" + str(i) + ".txt", "a") as outputfile:
                        outputfile.write("\t".join(row) + "\n")
                    not_found += 1
    print("Number of records that could not be placed in a clade and were assigned '?': " + str(not_found) + "/" + str(total))

print("Done.")
