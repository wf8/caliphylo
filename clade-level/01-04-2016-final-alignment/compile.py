#! /usr/bin/python
"""
Script to compile sequence matrix for all clades.
    - Should minimize chimeric OTUs by using species with the most 
        CBP sequences
    - generate csv spreadsheet with all accessions
    - output any clades missing sequence data
    - realign each gene region using MAFFT
    - produce concatenated alignment
"""

import csv
from Bio import Alphabet
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from os import listdir
from os.path import isfile, join

seq_files = ["Californian master sequences/California_18S_master.fasta",
         "Californian master sequences/California_ITS_master.fasta",
         "Californian master sequences/California_atpB_master.fasta",
         "Californian master sequences/California_matK_master.fasta",
         "Californian master sequences/California_ndhF_master.fasta",
         "Californian master sequences/California_rbcL_master.fasta",
         "Californian master sequences/California_trnL_trnF_master.fasta"]

clade_file = "Californian master sequences/Californian_Clade_Masterlist.csv"

clades_with_no_data = []

def get_binomial(description):
    words = description.split("_")
    return words[0] + "_" + words[1]

def get_accession(description):
    if "_CBP" in description:
        return "CBP"
    else:
        words = description.split("_")
        if "subsp." in words[2] or "var." in words[2]:
            return words[4]
        else:
            return words[2]




print("Getting list of all clades/species...")
clades = {} # dictionary with clade name as key and list of species binomials as value
with open(clade_file, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for i, row in enumerate(csvreader):
        if i != 0:
            clade = row[1]
            if clade not in clades:
                clades[clade] = []
            clades[clade].append(row[0])


print("Looping through all clades and gathering available sequences...")
clade_sequences = {} # dictionary with clade name as key and list of lists of seq records as value
clade_binomials = {}
for clade in clades.iterkeys():
    clade_sequences[clade] = [ [],[],[],[],[],[],[] ]
    clade_binomials[clade] = [ [],[],[],[],[],[],[] ]
for i, seq_file in enumerate(seq_files):
    handle = open(seq_file, "rU")
    for record in SeqIO.parse(handle, "fasta"):
        description = str(record.description)
        binomial = get_binomial(description)
        for clade in clades.iterkeys():
            if binomial in clades[clade] and binomial not in clade_binomials[clade][i]:
                clade_sequences[clade][i].append(record)
                clade_binomials[clade][i].append(binomial)
                break

print("Picking best sequences for each clade...")
clade_best_sequences = {}
for clade in clades.iterkeys():
    clade_best_sequences[clade] = []
    species_with_most_sequences = ""
    most_sequences = 0
    species = {}
    # find species with most sequences across all gene regions
    for i in range(7):
        for record in clade_sequences[clade][i]:
            description = str(record.description)
            binomial = get_binomial(description)
            if binomial not in species:
                species[binomial] = 1
            else:
                species[binomial] += 1
            if species[binomial] > most_sequences:
                species_with_most_sequences = binomial
                most_sequences = species[binomial]
    # now pick the final sequences for this clade, preferring the one with the most seq
    for i in range(7):
        preferred_found = False
        for record in clade_sequences[clade][i]:
            description = str(record.description)
            binomial = get_binomial(description)
            if binomial == species_with_most_sequences:
                clade_best_sequences[clade].append(record)
                preferred_found = True
                break
        if not preferred_found:
            # pick a CBP sequence if possible
            CBP_found = False
            for record in clade_sequences[clade][i]:
                description = str(record.description)
                if get_accession(description) == "CBP":
                    clade_best_sequences[clade].append(record)
                    CBP_found = True
                    break
            if not CBP_found:
                if len(clade_sequences[clade][i]) > 0:
                    clade_best_sequences[clade].append(clade_sequences[clade][i][0])
                else:
                    clade_best_sequences[clade].append("")

print("Generating spreadsheet of accessions...")
csv_rows = []
csv_rows.append(["clade", "18S", "ITS", "atpB", "matK", "ndhF", "rbcL", "trnL_trnF"])
for clade in clades.iterkeys():
    row = []
    row.append(clade)
    found = False
    for record in clade_best_sequences[clade]:
        if record == "":
            row.append("")
        else:
            description = str(record.description)
            row.append(get_accession(description))
            found = True
    csv_rows.append(row)
    if not found:
        clades_with_no_data.append(clade)
        print("No sequence data found for clade: " + clade)
with open("accessions.csv", "wb") as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in csv_rows:
        csvwriter.writerow(row)

print("Making unaligned FASTA files of each gene...")
for i in range(7):
    records = []
    for clade in clades.iterkeys():
        if clade_best_sequences[clade][i] != "":
            records.append(clade_best_sequences[clade][i])
    output_handle = open("unaligned/" + str(i) + ".fasta", "w")
    SeqIO.write(records, output_handle, "fasta")


print("Aligning each gene...")
unaligned = [ f for f in listdir("unaligned/") if isfile(join("unaligned/",f)) ]
for f in unaligned:
    # align using MAFFT
    mafft_cline = MafftCommandline(input="unaligned/" + f)
    mafft_cline.set_parameter("--auto", True)
    mafft_cline.set_parameter("--adjustdirection", True)
    print(str(mafft_cline))
    stdout, stderr = mafft_cline()
    with open("aligned/" + f, "w") as handle:
        handle.write(stdout)

raw_input("If necessary, you should now manually trim each alignment and then press enter to continue...")

print("Reading in aligned FASTA files for each gene....")
aligned = [ f for f in listdir("aligned/") if isfile(join("aligned/",f)) ]
alignment_lengths = []
clade_sequences = {} # dictionary with clade name as key and list of seq strings as value
for clade in clades.iterkeys():
    clade_sequences[clade] = ["","","","","","",""]
for i, seq_file in enumerate(aligned):
    handle = open("aligned/" + seq_file, "rU")
    length = 0
    for record in SeqIO.parse(handle, "fasta"):
        length = len(str(record.seq))
        description = str(record.description)
        #print description
        binomial = get_binomial(description)
        for clade in clades.iterkeys():
            if binomial in clades[clade]:
                clade_sequences[clade][i] = str(record.seq)
                break
    alignment_lengths.append(length)

# partition file format:
# DNA, p1=1-30
# DNA, p2=31-60
print("Generating partition file...")
f = open("partitions.txt", "w")
start = 1
for i, l in enumerate(alignment_lengths):
    f.write("DNA, p" + str(i + 1) + "=" + str(start) + "-" + str(l) + "\n")
    start += l
f.close()

print("Concatenating alignments....")
final_records = []
for clade in clades.iterkeys():
    if clade not in clades_with_no_data:
        final_seq = ""
        for i, seq in enumerate(clade_sequences[clade]):
            if seq == "":
                final_seq += "?" * alignment_lengths[i]
            else:
                final_seq += seq
        clade_name = clade.replace(" ", "_").replace("+","_plus_").replace("-","")
        final_records.append(SeqRecord(Seq(final_seq, alphabet=Alphabet.generic_dna), id=clade_name, description=""))

output_handle = open("concatenated.fasta", "w")
SeqIO.write(final_records, output_handle, "fasta")
output_handle = open("concatenated.nexus", "w")
SeqIO.write(final_records, output_handle, "nexus")
output_handle = open("concatenated.phy", "w")
SeqIO.write(final_records, output_handle, "phylip-relaxed")

print("Done.")
