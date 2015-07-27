#! /usr/bin/python

from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline

SeqIO.convert("collinsia_org_aligned.nex", "nexus", "collinsia_aligned.phy", "phylip-relaxed")

#print("Reading in original nexus file...")
#SeqIO.convert("allium_org_alignment.nex", "nexus", "allium_unaligned.fasta", "fasta")

#print("Aligning with MAFFT...")
#mafft_cline = MafftCommandline("allium_unaligned.fasta")
#mafft_cline.set_parameter("--auto", True)
#mafft_cline.set_parameter("--adjustdirection", True)
#print(str(mafft_cline))
#stdout, stderr = mafft_cline()

#print("Writing alignment to FASTA file...")
#with open("allium_aligned.fasta", "w") as handle:
#    handle.write(stdout)

#print("Making final phylip-relaxed file...")
#SeqIO.convert("allium_aligned.fasta", "fasta", "allium_aligned.phy", "phylip-relaxed")

#print("Done.")
