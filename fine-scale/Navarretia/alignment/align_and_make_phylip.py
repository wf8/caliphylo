#! /usr/bin/python

import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC




print('Concatenating...')
taxa = []
final_sequences = []
records_list = [list(SeqIO.parse('by_gene/ITS.fasta', 'fasta')), list(SeqIO.parse('by_gene/cpDNA.fasta', 'fasta')), list(SeqIO.parse('by_gene/g3pdh.fasta', 'fasta')),
           list(SeqIO.parse('by_gene/idhA.fasta', 'fasta')), list(SeqIO.parse('by_gene/idhB.fasta', 'fasta'))]

def get_unknowns(length):
    x = ''
    for i in range(length):
        x += '?'
    return x

# get list of all taxa
for records in records_list:
    for record in records:
        taxon = record.description
        if taxon not in taxa:
            taxa.append(taxon)
            final_sequences.append('')

# now concatenate
for records in records_list:
    for i, taxon in enumerate(taxa):
        found = False
        for record in records:
            if record.description == taxon:
                found = True
                final_sequences[i] += str(record.seq)
                break
        if not found:
            final_sequences[i] += get_unknowns(len(str(records[0].seq)))

# make final seq records
final_records = []
for i in range(len(final_sequences)):
    name = taxa[i].replace(' ', '_') 
    final_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=name))

print("Making final phylip-relaxed file...")
SeqIO.write(final_records, "navarretia_aligned.phy", "phylip-relaxed")

print("Done.")
