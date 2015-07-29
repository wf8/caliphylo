
import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from time import sleep

# taxon,trnG-trnR,atpA,rbcL

taxa = []
trnGR_accessions = []
atpA_accessions = []
rbcL_accessions = []

print('Reading in csv file...')
with open('myriopteris_accessions.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != 'taxon':
            taxa.append(row[0])
            trnGR_accessions.append(row[1])
            atpA_accessions.append(row[2])
            rbcL_accessions.append(row[3])

print('Reading in alignments...')
accessions = [trnGR_accessions, atpA_accessions, rbcL_accessions]
records = [list(SeqIO.parse('trnGR_aligned.fasta', 'fasta')), list(SeqIO.parse('atpA_aligned.fasta', 'fasta')), list(SeqIO.parse('rbcL_aligned.fasta', 'fasta'))]

for i, taxon in enumerate(taxa):
    print('\n' + taxon)
    found = False
    for record in records[0]:
        if trnGR_accessions[i] in record.description:
            found = True
            print(record.description)
            break
    if found == False:
        print('trnGR accession not found: ' + trnGR_accessions[i])
    found = False
    for record in records[1]:
        if atpA_accessions[i] in record.description:
            found = True
            print(record.description)
            break
    if found == False:
        print('atpA accession not found: ' + atpA_accessions[i])
    found = False
    for record in records[2]:
        if rbcL_accessions[i] in record.description:
            found = True
            print(record.description)
            break
    if found == False:
        print('rbcL accession not found: ' + rbcL_accessions[i])


print("Done.")
