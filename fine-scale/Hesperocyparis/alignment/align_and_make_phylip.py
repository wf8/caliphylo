#! /usr/bin/python

from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline

SeqIO.convert("Hesperocyparis_org_alignment.nex", "nexus", "hesperocyparis_alignment.phy", "phylip-relaxed")

