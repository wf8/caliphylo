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

print("Aligning ETS with MAFFT...")
mafft_cline = MafftCommandline(input="ETS_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing ETS alignment to FASTA file...")
with open("ETS_aligned.fasta", "w") as handle:
    handle.write(stdout)

print("Aligning trnK with MAFFT...")
mafft_cline = MafftCommandline(input="trnK_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing trnK alignment to FASTA file...")
with open("trnK_aligned.fasta", "w") as handle:
    handle.write(stdout)



print('Concatenating...')
taxa = []
final_sequences = []
records = [list(SeqIO.parse('ITS_aligned.fasta', 'fasta')), list(SeqIO.parse('ETS_aligned.fasta', 'fasta')), list(SeqIO.parse('trnK_aligned.fasta', 'fasta'))]

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

ETS_taxa = []
for ETS_record in records[1]:
    taxon = get_taxon_name(ETS_record.description, 'external')
    if taxon not in taxa:
        ETS_taxa.append(taxon)
        taxa.append(taxon)
        final_sequences.append(get_unknowns(len(str(records[0][0].seq))) + str(ETS_record.seq))
    else:
        for i, name in enumerate(taxa):
            if name == taxon:
                ETS_taxa.append(taxon)
                final_sequences[i] += str(ETS_record.seq)
                break
for i, taxon in enumerate(taxa):
    if taxon not in ETS_taxa:
        final_sequences[i] += get_unknowns(len(str(records[1][0].seq)))


trnK_taxa = []
for trnK_record in records[2]:
    taxon = get_taxon_name(trnK_record.description, 'trnK')
    if taxon not in taxa:
        trnK_taxa.append(taxon)
        taxa.append(taxon)
        final_sequences.append(get_unknowns(len(str(records[0][0].seq))) + get_unknowns(len(str(records[1][0].seq))) + str(trnK_record.seq))
    else:
        for i, name in enumerate(taxa):
            if name == taxon:
                trnK_taxa.append(taxon)
                final_sequences[i] += str(trnK_record.seq)
                break
for i, taxon in enumerate(taxa):
    if taxon not in trnK_taxa:
        final_sequences[i] += get_unknowns(len(str(records[2][0].seq)))


final_records = []
for i in range(len(final_sequences)):
    name = taxa[i].replace(' ', '_') 
    final_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=name))

print("Making final phylip-relaxed file...")
SeqIO.write(final_records, "lasthenia_aligned.phy", "phylip-relaxed")

print("Done.")
