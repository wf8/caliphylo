#! /usr/bin/python

import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

taxa = []
ITS1_accessions = []
ITS2_accessions = []

print('Reading in csv file...')
with open('asarum.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != 'taxon':
            taxa.append(row[0])
            ITS1_accessions.append(row[1])
            ITS2_accessions.append(row[2])

Entrez.email = 'freyman@berkeley.edu'

ITS1_records = []
ITS2_records = []

print('Downloading accessions...')
for accession in ITS1_accessions:
    handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
    ITS1_records.append(SeqIO.read(handle, 'fasta'))
    handle.close()
SeqIO.write(ITS1_records, "ITS1_unaligned.fasta", "fasta")

for accession in ITS2_accessions:
    handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
    ITS2_records.append(SeqIO.read(handle, 'fasta'))
    handle.close()
SeqIO.write(ITS2_records, "ITS2_unaligned.fasta", "fasta")

print("Aligning ITS1 with MAFFT...")
mafft_cline = MafftCommandline(input="ITS1_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing ITS1 alignment to FASTA file...")
with open("ITS1_aligned.fasta", "w") as handle:
    handle.write(stdout)

print("Aligning ITS2 with MAFFT...")
mafft_cline = MafftCommandline(input="ITS2_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing ITS2 alignment to FASTA file...")
with open("ITS2_aligned.fasta", "w") as handle:
    handle.write(stdout)

print('Concatenating...')
ITS1 = SeqIO.parse('ITS1_aligned.fasta', 'fasta')
ITS2 = SeqIO.parse('ITS2_aligned.fasta', 'fasta')
final_species = []
final_sequences = []
for record in ITS1:
    description = record.description
    start = description.find(' ') + 1
    end = description.find(' internal')
    taxon = description[start:end].replace(' ', '_')
    final_species.append(taxon)
    final_sequences.append(str(record.seq))

for record in ITS2:
    description = record.description
    start = description.find(' ') + 1
    end = description.find(' internal')
    taxon = description[start:end].replace(' ', '_')
    for i, species in enumerate(final_species):
        if taxon == species:
            final_sequences[i] = final_sequences[i] + str(record.seq)

final_records = []
for i in range(len(final_sequences)):
    final_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=final_species[i]))

print("Making final phylip-relaxed file...")
SeqIO.write(final_records, "asarum_aligned.phy", "phylip-relaxed")
#SeqIO.convert("allium_aligned.fasta", "fasta", "allium_aligned.phy", "phylip-relaxed")

print("Done.")
