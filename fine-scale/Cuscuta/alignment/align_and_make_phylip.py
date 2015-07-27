#! /usr/bin/python

from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline

SeqIO.convert("Cuscata_org_alignment_no_indels.nex", "nexus", "cuscuta_aligned.phy", "phylip-relaxed")

