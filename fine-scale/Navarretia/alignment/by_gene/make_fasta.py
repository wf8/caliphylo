#! /usr/bin/python

from Bio import SeqIO

SeqIO.convert("ITS.nex", "nexus", "ITS.fasta", "fasta")
SeqIO.convert("cpDNA.nex", "nexus", "cpDNA.fasta", "fasta")
SeqIO.convert("g3pdh.nex", "nexus", "g3pdh.fasta", "fasta")
SeqIO.convert("idhA.nex", "nexus", "idhA.fasta", "fasta")
SeqIO.convert("idhB.nex", "nexus", "idhB.fasta", "fasta")

