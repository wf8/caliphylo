#! /usr/bin/python

from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline

SeqIO.convert("montieae_org_alignment.nex", "nexus", "montieae_alignment.phy", "phylip-relaxed")

