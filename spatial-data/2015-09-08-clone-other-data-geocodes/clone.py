#! /usr/bin/python
"""
script to clone georeferences:
    find records for which the locality, date, and collector are the same
    and clone lat/lon coordinates for all those records 
    also add a yes/no field for cloned georeferences
"""

import csv
import codecs

org_files = ["input/combined_sources_August_24.csv"]

class Record:

    def __init__(self):
        self.year = ""
        self.month = ""
        self.day = ""
        self.collector = ""
        self.locality = ""
        self.lat = ""
        self.lon = ""

def convert_date(date):
    """
    takes as input '1963 May 04' and returns ['1963', '5', '4']
    """
    if date == '[collection date not given]' or date == '[no collection date given].' or '[no collection date given]':
        return ['', '', '']
    if date == 'June 12-16, 1948':
        return ['1948', '6', '12']
    # check for input in form '1925-04-31'
    if '-' in date:
        words = date.split('-')
        if len(words) == 3:
            return [words[0], words[1], words[2]]
        elif len(words) == 2:
            return [words[0], words[1], '']
        elif len(words) == 1:
            return [words[0], '', '']
    # check for input in form '4/24/1940'
    if '/' in date:
        words = date.split('/')
        return [words[2], words[0], words[1]]
    months = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    words = date.split(' ')
    if len(words) == 2:
        return [words[0], months[words[1].title()], '']
    elif len(words) == 1:
        return [words[0], '', '']
    else:
        return [words[0], months[words[1].title()], words[2]]

# column indexes
lon = 20
lat = 21
locality = 36
collector = 40
year = 41
month = 42
day = 43
date = 44

print("Reading other data sources tab delimited file...")
complete_records = []
num_records = 0
num_not_geocoded = 0
with open(org_files[0], 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        if num_records != 0:
            if row[lon] == '':
                num_not_geocoded += 1
            if row[lon] != '' and row[lat] != '' and row[locality] != '' and row[year] != '' and row[month] != '' and row[day] != '':
                record = Record()
                record.year = row[year]
                record.month = row[month]
                record.day = row[day]
                record.collector = row[collector]
                record.locality = row[locality]
                record.lat = row[lat]
                record.lon = row[lon]
                complete_records.append(record)
            elif row[lon] != '' and row[lat] != '' and row[locality] != '' and row[date] != '' and row[year] == '' and row[month] == '' and row[day] == '':
                the_date = convert_date(row[date])
                record = Record()
                record.year = the_date[0]
                record.month = the_date[1]
                record.day = the_date[2]
                record.collector = row[collector]
                record.locality = row[locality]
                record.lat = row[lat]
                record.lon = row[lon]
                complete_records.append(record)
        num_records += 1

print("Total number of records: " + str(num_records))
print("Number of records not geocoded: " + str(num_not_geocoded))
print("Number of geocoded records with dates: " + str(len(complete_records)))

print("Cloning georeferences...")
cloned_records = 0
row_num = 0
with open(org_files[0], 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        if row_num != 0:
            if row[date] != '' and row[year] == '' and row[month] == '' and row[day] == '':
                the_date = convert_date(row[date])
                row[year] = the_date[0]
                row[month] = the_date[1]
                row[day] = the_date[2]
            cloned = False
            if row[lon] == '' and row[lat] == '' and row[locality] != '' and row[year] != '' and row[month] != '' and row[day] != '':
                for record in complete_records:
                    try:
                        if int(record.year) == int(row[year]) and int(record.month) == int(row[month]) and int(record.day) == int(row[day]) and record.locality == row[locality]:
                            cloned_records += 1
                            row[lat] = record.lat
                            row[lon] = record.lon
                            cloned = True
                            break
                    except:
                        try:
                            if int(record.year) == int(row[year]) and int(record.month) == int(row[month]) and record.locality == row[locality]:
                                cloned_records += 1
                                row[lat] = record.lat
                                row[lon] = record.lon
                                cloned = True
                                break
                        except:
                            try:
                                if int(record.year) == int(row[year]) and record.locality == row[locality]:
                                    cloned_records += 1
                                    row[lat] = record.lat
                                    row[lon] = record.lon
                                    cloned = True
                                    break
                            except:
                                continue
            if cloned:
                row.append('yes')
            else:
                row.append('no')
        else:
            row.append('cloned_georeference')
        row_num += 1
        with open("output/combined_sources_cloned_Sept_08.txt", "a") as outputfile:
            outputfile.write("\t".join(row) + "\n")
print("Number of cloned records: " + str(cloned_records))

print("Done.")
