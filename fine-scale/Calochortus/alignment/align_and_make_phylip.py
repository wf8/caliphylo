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
trnTL_accessions = []
trnL_accessions = []
trnLF_accessions = []
psbA_accessions = []
rpl16_accessions = []

print('Reading in csv file...')
with open('calochortus_accessions.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != 'taxon':
            taxa.append(row[0])
            trnTL_accessions.append(row[1])
            trnL_accessions.append(row[2])
            trnLF_accessions.append(row[3])
            psbA_accessions.append(row[4])
            rpl16_accessions.append(row[5])

trnTL_records = []
trnL_records = []
trnLF_records = []
psbA_records = []
rpl16_records = []
Entrez.email = 'freyman@berkeley.edu'

print('Downloading accessions...')
for accession in trnTL_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        trnTL_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(trnTL_records, "trnTL_unaligned.fasta", "fasta")

for accession in trnL_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        trnL_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(trnL_records, "trnL_unaligned.fasta", "fasta")

for accession in trnLF_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        trnLF_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(trnLF_records, "trnLF_unaligned.fasta", "fasta")

for accession in psbA_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        psbA_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(psbA_records, "psbA_unaligned.fasta", "fasta")

for accession in rpl16_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        rpl16_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(rpl16_records, "rpl16_unaligned.fasta", "fasta")

print("Aligning trnTL with MAFFT...")
mafft_cline = MafftCommandline(input="trnTL_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing trnTL alignment to FASTA file...")
with open("trnTL_aligned.fasta", "w") as handle:
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

print("Aligning trnLF with MAFFT...")
mafft_cline = MafftCommandline(input="trnLF_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing trnLF alignment to FASTA file...")
with open("trnLF_aligned.fasta", "w") as handle:
    handle.write(stdout)

print("Aligning psbA with MAFFT...")
mafft_cline = MafftCommandline(input="psbA_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing psbA alignment to FASTA file...")
with open("psbA_aligned.fasta", "w") as handle:
    handle.write(stdout)

print("Aligning rpl16 with MAFFT...")
mafft_cline = MafftCommandline(input="rpl16_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing rpl16 alignment to FASTA file...")
with open("rpl16_aligned.fasta", "w") as handle:
    handle.write(stdout)

print('Concatenating...')
accessions = [trnTL_accessions, trnL_accessions, trnLF_accessions, psbA_accessions, rpl16_accessions]
records = [list(SeqIO.parse('trnTL_aligned.fasta', 'fasta')), list(SeqIO.parse('trnL_aligned.fasta', 'fasta')), list(SeqIO.parse('trnLF_aligned.fasta', 'fasta')),
           list(SeqIO.parse('psbA_aligned.fasta', 'fasta')), list(SeqIO.parse('rpl16_aligned.fasta', 'fasta'))]

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
    final_records.append(SeqRecord(Seq(final_sequences[i], IUPAC.ambiguous_dna), id=taxa[i]))

print("Making final phylip-relaxed file...")
SeqIO.write(final_records, "calochortus_aligned.phy", "phylip-relaxed")
#SeqIO.convert("allium_aligned.fasta", "fasta", "allium_aligned.phy", "phylip-relaxed")

print("Done.")
