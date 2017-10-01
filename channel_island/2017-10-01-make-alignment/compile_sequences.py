#! /usr/bin/python

#
# Script to generate alignment combining GenBank mined sequence data
# with CIPP sequence data.
#


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
CIPP_genes = ['ITS', 'matK', 'rbcL']
#genes = ['ITS']
#CIPP_genes = ['ITS']
accessions = []
records = []
for gene in genes:
    accessions.append([])
    records.append([])

print('Reading in GenBank accessions csv file...')
with open('data/genbank_accessions.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != 'taxon':
            taxa.append(row[0].replace(".","").replace(" ","_"))
            for i, gene in enumerate(genes):
                accessions[i].append(row[i + 1])

print('Reading in CIPP sequence data...')
CIPP_taxa = []
for gene in CIPP_genes:
    sequences = list(SeqIO.parse("data/CIPP_endemics_" + gene + ".fasta", "fasta"))
    for seq in sequences:
        if seq.description not in CIPP_taxa:
            CIPP_taxa.append(seq.description.replace(".","").replace(" ","_"))

total_taxa = []
for taxon in taxa:
    if taxon not in total_taxa:
        total_taxa.append(taxon)
for taxon in CIPP_taxa:
    if taxon not in total_taxa:
        total_taxa.append(taxon)

total_accessions = []
print('Combining and aligning each gene...')
for i, gene in enumerate(genes):
    
    unaligned_records = []
    total_accessions.append([""] * len(total_taxa))

    gb_records = list(SeqIO.parse("data/aligned" + gene + ".fasta", "fasta"))

    # check all taxa from the GenBank data
    for j, taxon in enumerate(taxa):
    
        sequence = ''
        if taxon in CIPP_taxa and gene in CIPP_genes:
            # check for a CIPP sequence
            sequences = list(SeqIO.parse("data/CIPP_endemics_" + gene + ".fasta", "fasta"))
            for seq in sequences:
                if taxon in seq.description:
                    sequence = str(record.seq)
                    total_accessions[i][ total_taxa.index(taxon) ] = "CIPP"
                    break
        
        if (sequence == ""):
            # check for a GenBank sequence
            if accessions[i][j].strip() == '':
                sequence += "?"
            else:
                for record in gb_records:
                    if accessions[i][j].strip() in record.description:
                        sequence = str(record.seq)
                        total_accessions[i][ total_taxa.index(taxon) ] = accessions[i][j].strip()
                        break
    
        unaligned_records.append(SeqRecord(Seq(sequence, IUPAC.ambiguous_dna), id=taxon, description="", name=""))
        
    # check all taxa from the CIPP data
    for j, taxon in enumerate(CIPP_taxa):

        if taxon not in taxa:

            sequence = ''
            if gene in CIPP_genes:
                # check for a CIPP sequence
                sequences = list(SeqIO.parse("data/CIPP_endemics_" + gene + ".fasta", "fasta"))
                for seq in sequences:
                    if taxon in seq.description:
                        sequence = str(record.seq)
                        total_accessions[i][ total_taxa.index(taxon) ] = "CIPP"
                        break
            
            unaligned_records.append(SeqRecord(Seq(sequence, IUPAC.ambiguous_dna), id=taxon, description="", name=""))

    # write the unaligned sequences for this gene
    SeqIO.write(unaligned_records, "data/unaligned_" + gene + ".fasta", "fasta")
    
    mafft_cline = MafftCommandline(input="data/unaligned_" + gene + ".fasta")
    mafft_cline.set_parameter("--auto", True)
    mafft_cline.set_parameter("--adjustdirection", True)
    print(str(mafft_cline))
    stdout, stderr = mafft_cline()

    print("Writing " + gene + " alignment to FASTA file...")
    with open("data/final_aligned_" + gene + ".fasta", "w") as handle:
        handle.write(stdout)
            



print('Concatenating...')
final_records = []
alignment_lengths = []
for i, gene in enumerate(genes):
    final_records.append(list(SeqIO.parse("data/final_aligned_" + gene + ".fasta", "fasta")))
    alignment_lengths.append( len(str(final_records[i][0].seq)) )

def get_unknowns(length):
    return '?' * length

final_sequences = []
for i, taxon in enumerate(total_taxa):
    sequence = ''
    for j, gene in enumerate(genes):
        if total_accessions[j][i].strip() == '':
            sequence += get_unknowns(len(str(final_records[j][0].seq)))
        else:
            for record in final_records[j]:
                if taxon == record.id:
                    sequence += str(record.seq)
                    break
    final_sequences.append(sequence)

concatenated_records = []
for i, taxon in enumerate(total_taxa):
    concatenated_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=taxon, description="", name=""))

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

with open("final_accessions.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["taxon"] + genes)
    for i, taxon in enumerate(total_taxa):
        r = [taxon]
        for j, gene in enumerate(genes):
            r.append(total_accessions[j][i])
        writer.writerow(r)

print("Done.")
