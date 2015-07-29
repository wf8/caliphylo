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
n = 1
for accession in ITS_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        record = SeqIO.read(handle, 'fasta')
        # >gi|2895483|gb|AF032007.1| Sanicula tracyi internal transcribed spacer 1, 5.8S ribosomal RNA gene, and internal transcribed spacer 2, complete sequence
        names = record.description.split('|')
        end = names[-1].find('internal')
        name = names[-1][1:end] + str(n)
        record.description = ''
        record.id = name.replace(' ', '_')
        ITS_records.append(record)
        handle.close()
        sleep(0.02)
        n += 1
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
