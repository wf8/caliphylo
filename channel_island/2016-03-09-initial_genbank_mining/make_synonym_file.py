#! /usr/bin/python

import csv

in_file = "ChI_species_list_030816.csv"

taxa = []
with open(in_file, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for i, row in enumerate(csvreader):
        if i != 0:
            taxon = []
            for j in [0, 4, 8, 12]:
                if row[j] != "" and row[j + 2] == "":
                    name = row[j] + " " + row[j + 1]
                    taxon.append(name)
                else:
                    if row[j + 2] == "ssp.":
                        name = row[j] + " " + row[j + 1] + " ssp. " + row[j + 3]
                        taxon.append(name)
                        name = row[j] + " " + row[j + 1] + " subsp. " + row[j + 3]
                        taxon.append(name)
                        name = row[j] + " " + row[j + 1] + " var. " + row[j + 3]
                        taxon.append(name)
                    if row[j + 2] == "var.":
                        name = row[j] + " " + row[j + 1] + " var. " + row[j + 3]
                        taxon.append(name)
                        name = row[j] + " " + row[j + 1] + " ssp. " + row[j + 3]
                        taxon.append(name)
                        name = row[j] + " " + row[j + 1] + " subsp. " + row[j + 3]
                        taxon.append(name)
            taxa.append(taxon)

with open("synonyms.csv", "wb") as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in taxa:
        csvwriter.writerow(row)
