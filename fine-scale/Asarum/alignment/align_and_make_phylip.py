#! /usr/bin/python

import csv
from Bio import Entrez
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC


print("Aligning ITS with MAFFT...")
mafft_cline = MafftCommandline(input="asarum_unaligned.fasta")
mafft_cline.set_parameter("--auto", True)
mafft_cline.set_parameter("--adjustdirection", True)
print(str(mafft_cline))
stdout, stderr = mafft_cline()

print("Writing ITS alignment to FASTA file...")
with open("asarum_aligned.fasta", "w") as handle:
    handle.write(stdout)


print("Making final phylip-relaxed file...")
SeqIO.convert("asarum_aligned.fasta", "fasta", "asarum_aligned.phy", "phylip-relaxed")

print("Done.")
