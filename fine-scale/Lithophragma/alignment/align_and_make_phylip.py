#! /usr/bin/python

import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC



print("Aligning ITS with MAFFT...")
mafft_cline = MafftCommandline(input="ITS_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing ITS alignment to FASTA file...")
with open("ITS_aligned.fasta", "w") as handle:
    handle.write(stdout)


print('Concatenating...')
taxa = []
final_sequences = []
records = [list(SeqIO.parse('ITS_aligned.fasta', 'fasta'))]

def get_unknowns(length):
    x = ''
    for i in range(length):
        x += '?'
    return x

def get_taxon_name(description, stop):
    # gi|18105175|gb|AF391622.1| Lasthenia platycarpha isolate plat139 internal transcribed spacer 1, 5.8S ribosomal RNA gene, and internal transcribed spacer 2, complete sequence
    words = description.split('|')
    end = words[-1].find(stop)
    return words[-1][1:end-1]

final_sequences = []
for ITS_record in records[0]:
    taxon = get_taxon_name(ITS_record.description, 'internal')
    if taxon not in taxa:
        taxa.append(taxon)
        final_sequences.append(str(ITS_record.seq))



final_records = []
for i in range(len(final_sequences)):
    name = taxa[i].replace(' ', '_') 
    final_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=name))

print("Making final phylip-relaxed file...")
SeqIO.write(final_records, "lithophragma_aligned.phy", "phylip-relaxed")

print("Done.")
