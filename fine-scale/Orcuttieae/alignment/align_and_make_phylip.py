#! /usr/bin/python

import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from time import sleep

# taxon,trnT-trnL_spacer,trnL_intron,trnL-trnF_spacer,psbA-trnH,rpl16

taxa = []
ITS1_accessions = []
ITS2_accessions = []
trnL_accessions = []

print('Reading in csv file...')
with open('orcuttieae_accessions.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != 'taxon':
            taxa.append(row[0])
            trnL_accessions.append(row[1])
            ITS1_accessions.append(row[2])
            ITS2_accessions.append(row[3])

ITS1_records = []
ITS2_records = []
trnL_records = []
Entrez.email = 'freyman@berkeley.edu'

print('Downloading accessions...')
for accession in ITS1_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        ITS1_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(ITS1_records, "ITS1_unaligned.fasta", "fasta")

for accession in ITS2_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        ITS2_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(ITS2_records, "ITS2_unaligned.fasta", "fasta")

for accession in trnL_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        trnL_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(trnL_records, "trnL_unaligned.fasta", "fasta")


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

print("Aligning trnL with MAFFT...")
mafft_cline = MafftCommandline(input="trnL_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing trnL alignment to FASTA file...")
with open("trnL_aligned.fasta", "w") as handle:
    handle.write(stdout)


print('Concatenating...')
accessions = [ITS1_accessions, ITS2_accessions, trnL_accessions]
records = [list(SeqIO.parse('ITS1_aligned.fasta', 'fasta')), list(SeqIO.parse('ITS2_aligned.fasta', 'fasta')), list(SeqIO.parse('trnL_aligned.fasta', 'fasta'))]

def get_unknowns(length):
    x = ''
    for i in range(length):
        x += '?'
    return x

final_sequences = []
for i, taxon in enumerate(taxa):
    sequence = ''
    for j, accession in enumerate(accessions):
        if accession[i].strip() == '':
            sequence += get_unknowns(len(str(records[j][0].seq)))
        else:
            for record in records[j]:
                if accession[i].strip() in record.description:
                    sequence += str(record.seq)
                    break
    final_sequences.append(sequence)

final_records = []
for i in range(len(final_sequences)):
    name = taxa[i].replace(' ', '_')
    final_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=name))

print("Making final phylip-relaxed file...")
SeqIO.write(final_records, "orcuttieae_aligned.phy", "phylip-relaxed")

print("Done.")
