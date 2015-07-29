#! /usr/bin/python

import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from time import sleep


ITS_accessions = []

print('Reading in csv file...')
with open('sanicula_ITS_accessions.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        ITS_accessions.append(row[0])

ITS_records = []
Entrez.email = 'freyman@berkeley.edu'

print('Downloading accessions...')
for accession in ITS_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        ITS_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(ITS_records, "ITS_unaligned.fasta", "fasta")

print("Aligning ITS with MAFFT...")
mafft_cline = MafftCommandline(input="ITS_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing ITS alignment to FASTA file...")
with open("ITS_aligned.fasta", "w") as handle:
    handle.write(stdout)

print("Making final phylip-relaxed file...")
SeqIO.convert("ITS_aligned.fasta", "fasta", "sanicula_aligned.phy", "phylip-relaxed")

print("Done.")
