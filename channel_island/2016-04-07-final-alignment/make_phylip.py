#! /usr/bin/python

import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from time import sleep

# taxon,ITS,matK,matR,ndhF,rbcL,trnL-trnF,18S,atpB,

taxa = []
genes = ['ITS','matK','matR','ndhF','rbcL','trnL-trnF','18S','atpB']
accessions = []
records = []
for gene in genes:
    accessions.append([])
    records.append([])

Entrez.email = 'freyman@berkeley.edu'

print('Reading in csv file...')
with open('accessions.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != 'taxon':
            taxa.append(row[0])
            for i, gene in enumerate(genes):
                accessions[i].append(row[i + 1])

#for i, gene in enumerate(genes):
#    print('Downloading ' + gene + ' accessions...')
#    for accession in accessions[i]:
#        if accession.strip() != '':
#            handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
#            records[i].append(SeqIO.read(handle, 'fasta'))
#            handle.close()
#            sleep(0.02)
#    SeqIO.write(records[i], 'unaligned_' + gene + '.fasta', 'fasta')
#
#for i, gene in enumerate(genes):
#    print("Aligning " + gene + " with MAFFT...")
#    mafft_cline = MafftCommandline(input="unaligned_" + gene + ".fasta")
#    mafft_cline.set_parameter("--auto", True)
#    mafft_cline.set_parameter("--adjustdirection", True)
#    print(str(mafft_cline))
#    stdout, stderr = mafft_cline()
#
#    print("Writing " + gene + " alignment to FASTA file...")
#    with open("aligned" + gene + ".fasta", "w") as handle:
#        handle.write(stdout)

print('Concatenating...')
final_records = []
alignment_lengths = []
for i, gene in enumerate(genes):
    final_records.append(list(SeqIO.parse("aligned" + gene + ".fasta", "fasta")))
    alignment_lengths.append( len(str(final_records[i][0].seq)) )

def get_unknowns(length):
    return '?' * length

final_sequences = []
for i, taxon in enumerate(taxa):
    sequence = ''
    for j, accession in enumerate(accessions):
        if accession[i].strip() == '':
            sequence += get_unknowns(len(str(final_records[j][0].seq)))
        else:
            for record in final_records[j]:
                if accession[i].strip() in record.description:
                    sequence += str(record.seq)
                    break
    final_sequences.append(sequence)

concatenated_records = []
for i in range(len(final_sequences)):
    concatenated_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=taxa[i].replace(" ", "_")))

print("Making final phylip-relaxed file...")
SeqIO.write(concatenated_records, "ci_alignment.phy", "phylip-relaxed")

# partition file format:
# DNA, p1=1-30
# DNA, p2=31-60
print("Generating partition file...")
f = open("ci_partitions.txt", "w")
start = 0
for i, l in enumerate(alignment_lengths):
    f.write("DNA, p" + str(i + 1) + "=" + str(start + 1) + "-" + str(l + start) + "\n")
    start += l
f.close()

print("Done.")
