#! /usr/bin/python
"""
script to remove CCH records from GBIF
"""

import csv
import codecs

org_file = "../org_spatial_data/GBIF August 5th 2015/GBiF Californian Spatial files/occurrence.txt"

collection_codes = ["BLMAR",
"CAS",
"DS",
"CATA",
"CDA",
"MACF",
"SFU",
"SACT",
"OBI",
"CSUSB",
"CHSC",
"HSC",
"JROH",
"JOTR",
"PASA",
"PGM",
"RSA",
"POM",
"CLARK-A",
"SCFS",
"JEPS",
"UC",
"SD",
"SDSU",
"SJSU",
"SBBG",
"GMDRC",
"UCD",
"IRVC",
"LA",
"UCLA",
"UCR",
"UCSB",
"UCSC",
"VVC",
"YM",
"HUH",
"Harvard University Herbarium",
"Harvard University",
"NY",
"SEIN",
"Californian Consortium"]


print("Checking for NULL bytes due to MS Excel...")
fi = open(org_file, 'rb')
data = fi.read()
fi.close()
if data.count('\x00') > 0:
    fo = open(org_file, 'wb')
    fo.write(data.replace('\x00', ''))
    fo.close()


print("Checking institution codes in GBIF database...")
genera = {}
with open(org_file, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
    found_column = False
    column = 0
    for row in csvreader:
        if not found_column:
            for i, thecolumn in enumerate(row):
                if thecolumn.strip() == "institutionCode":
                    column = i
                    found_column = True
                if thecolumn.strip() == "collectionCode":
                    column2 = i
        institution_code = row[column].strip()
        collection_id = row[column2].strip()
        if institution_code not in collection_codes and collection_id not in collection_codes:
            with open("gbif_purged.txt", "a") as outputfile:
                outputfile.write("\t".join(row) + "\n")

print("Done.")
