
import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from time import sleep

# taxon,trnG-trnR,atpA,rbcL

taxa = []
trnGR_accessions = []
atpA_accessions = []
rbcL_accessions = []

print('Reading in csv file...')
with open('myriopteris_accessions_corrected.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != 'taxon':
            taxa.append(row[0])
            trnGR_accessions.append(row[1])
            atpA_accessions.append(row[2])
            rbcL_accessions.append(row[3])

trnGR_records = []
atpA_records = []
rbcL_records = []
Entrez.email = 'freyman@berkeley.edu'

print('Downloading accessions...')
for accession in trnGR_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        trnGR_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(trnGR_records, "trnGR_unaligned.fasta", "fasta")

for accession in atpA_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        atpA_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(atpA_records, "atpA_unaligned.fasta", "fasta")

for accession in rbcL_accessions:
    if accession.strip() != '':
        handle = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text', id=accession)
        rbcL_records.append(SeqIO.read(handle, 'fasta'))
        handle.close()
        sleep(0.02)
SeqIO.write(rbcL_records, "rbcL_unaligned.fasta", "fasta")


print("Aligning atpA with MAFFT...")
mafft_cline = MafftCommandline(input="atpA_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing atpA alignment to FASTA file...")
with open("atpA_aligned.fasta", "w") as handle:
    handle.write(stdout)

print("Aligning rbcL with MAFFT...")
mafft_cline = MafftCommandline(input="rbcL_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing rbcL alignment to FASTA file...")
with open("rbcL_aligned.fasta", "w") as handle:
    handle.write(stdout)

print("Aligning trnGR with MAFFT...")
mafft_cline = MafftCommandline(input="trnGR_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing trnGR alignment to FASTA file...")
with open("trnGR_aligned.fasta", "w") as handle:
    handle.write(stdout)


print('Concatenating...')
accessions = [trnGR_accessions, atpA_accessions, rbcL_accessions]
records = [list(SeqIO.parse('trnGR_aligned.fasta', 'fasta')), list(SeqIO.parse('atpA_aligned.fasta', 'fasta')), list(SeqIO.parse('rbcL_aligned.fasta', 'fasta'))]

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
SeqIO.write(final_records, "myriopteris_aligned.phy", "phylip-relaxed")

print("Done.")
