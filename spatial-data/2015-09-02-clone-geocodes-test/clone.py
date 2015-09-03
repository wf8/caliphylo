#! /usr/bin/python
"""
script to clone geocodes:
    find records for which the locality and date are the same
    and clone lat/lon coordinates for all those records 
    also add a yes/no field for cloned geocodes
"""

import csv
import codecs

org_files = ["input/CCH_clades_by_counties_Part_01.csv"]

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
    deals with dates in two formats: 10/18/1990 and 1878-2-11
    return ['1878', '2', '11']
    """
    # first deal with any oddball exceptions
    if date == '[collection date not given]' or date == '[no collection date given].' or date == '[no collection date given]':
        return ['', '', '']
    if date == 'June 12-16, 1948':
        return ['1948', '6', '12']
    date = date.replace('.', '')
    date = date.replace(',', '')
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
        try:
            return [words[2], words[0], words[1]]
        except:
            return [words[1], words[0], '']
    months = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12',
                'January':'1','February':'2','March':'3','April':'4','June':'6','July':'7','August':'8','September':'9','October':'10','November':'11','December':'12',
                'Sept':'9', 'Mch':'3'}
    words = date.split(' ')
    # check for format '1919 Month 5 Day 19'
    if 'Month' in date:
        return [words[0], words[2], words[4]]
    # check for format '5 18 1963'
    if len(words[0]) < 3:
        try:
            return [words[2], words[0], words[1]]
        except:
            return [words[1], words[0], '']
    # finally deal with format 'Mar 5 1950'
    if len(words) == 2:
        print words
        return [words[1], months[words[0].title()], '']
    elif len(words) == 1:
        return [words[0], '', '']
    else:
        return [words[2], months[words[0].title()], words[1]]

# column indexes
lon = 17
lat = 18
locality = 15
collector = 5
#year = 40
#month = 41
#day = 42
date = 10

print("Reading in CCH_clades_by_counties_Part_01.csv...")
complete_records = []
num_records = 0
num_records_geocoded = 0
with open(org_files[0], 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        if num_records != 0:
            if row[lon] != '' and row[lat] != '' and row[locality] != '' and row[date] != '':
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
        if row[lon] != '':
            num_records_geocoded += 1

print("Total number of records: " + str(num_records))
print("Initial number of geocoded records: " + str(num_records_geocoded))
print("Initial number of geocoded records with dates and locality: " + str(len(complete_records)))

print("Cloning geocodes...")
cloned_records = 0
row_num = 0
with open(org_files[0], 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        if row_num != 0:
            cloned = False
            if row[lon] == '' and row[lat] == '' and row[locality] != '' and row[date] != '':
                the_date = convert_date(row[date])
                row_year = the_date[0]
                row_month = the_date[1]
                row_day = the_date[2]
                for record in complete_records:
                    try:
                        if int(record.year) == int(row_year) and int(record.month) == int(row_month) and int(record.day) == int(row_day) and record.locality == row[locality]:
                            cloned_records += 1
                            row[lat] = record.lat
                            row[lon] = record.lon
                            cloned = True
                            break
                    except:
                        try:
                            if int(record.year) == int(row_year) and int(record.month) == int(row_month) and record.locality == row[locality]:
                                cloned_records += 1
                                row[lat] = record.lat
                                row[lon] = record.lon
                                cloned = True
                                break
                        except:
                            try:
                                if int(record.year) == int(row_year) and record.locality == row[locality]:
                                    cloned_records += 1
                                    row[lat] = record.lat
                                    row[lon] = record.lon
                                    cloned = True
                                    break
                            except Exception as e:
                                print("Error:")
                                print(row)
                                print(record.year + " comparison with " + row_year)
                                print(e)
                                #continue
            if cloned:
                row.append('yes')
            else:
                row.append('no')
        else:
            row.append('cloned_geocode')
        row_num += 1
        with open("output/CCH_clades_by_counties_Part_01.txt", "a") as outputfile:
            outputfile.write("\t".join(row) + "\n")
print("Number of newly cloned records: " + str(cloned_records))
print("New total number of geocoded records: " + str(cloned_records + num_records_geocoded))
print("Percent of geocodes newly cloned: " + str(round(float(cloned_records * 100)/float(cloned_records + num_records_geocoded), 2)))

print("Done.")
