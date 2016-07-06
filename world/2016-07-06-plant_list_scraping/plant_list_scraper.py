#! /usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import csv
import requests
import time
import sys

links = ["http://www.theplantlist.org/1.1/browse/-/-/"]


accepted_out = "accepted_genera.csv"
unresolved_out = "unresolved_genera.csv"

def get_data(link):

    page = requests.get(link)
    page.encoding = 'utf-8'
    source = page.text
    
    # <a href="/1.1/browse/A/Caprifoliaceae/Abelia/"><i class="Accepted genus">Abelia</i></a> (<i class="family">Caprifoliaceae</i>)

    # find all accepted genera
    genera = []
    families = []
    begin = 0
    end = 0
    done = False
    while (done == False):
        begin = source.find('<i class="Accepted genus">', end)
        if begin == -1:
            done = True
        else:
            end = source.find('</i>', begin)
            genus = source[begin + 26:end].replace(u'×&nbsp;', u'')
            if genus not in genera:
                genera.append(genus)
                begin = source.find('<i class="family">', end)
                end = source.find('</i>', begin)
                family = source[begin + 18:end]
                families.append(family)

    # make csv file
    with open(accepted_out, 'wb') as csvfile:
        for i in range( len(genera) ):
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([genera[i].encode('utf-8'), families[i].encode('utf-8')])
    
    # find all unresolved genera
    genera = []
    families = []
    begin = 0
    end = 0
    done = False
    while (done == False):
        begin = source.find('<i class="Unresolved genus">', end)
        if begin == -1:
            done = True
        else:
            end = source.find('</i>', begin)
            genus = source[begin + 28:end].replace(u'×&nbsp;', u'')
            if genus not in genera:
                genera.append(genus)
                begin = source.find('<i class="family">', end)
                end = source.find('</i>', begin)
                family = source[begin + 18:end]
                families.append(family)

    # make csv file
    with open(unresolved_out, 'wb') as csvfile:
        for i in range( len(genera) ):
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([genera[i].encode('utf-8'), families[i].encode('utf-8')])



for link in links:
    try:
        get_data(link)
    except Exception as e:
        # need to retry
        time.sleep(0.5)
        get_data(link)



