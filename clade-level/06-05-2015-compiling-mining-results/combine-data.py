
from Bio import SeqIO

gene_labels = ["18S","atpB","ndhF","trnL-trnF"]
org_files = ["data-from-Andrew/California_species_18S.fasta","data-from-Andrew/California_species_atpB.fasta",\
             "data-from-Andrew/California_species_ndhF.fasta","data-from-Andrew/California_species_trnL_trnF.fasta"]
new_alignments = ["aligned_18S.fasta","aligned_atpB.fasta","aligned_ndhF.fasta","aligned_trnL-trnF.fasta"]
gene_records = [[],[],[],[]]

for i in range(4):
    for record in SeqIO.parse(open(org_files[i], "rU"), "fasta"):
        gene_records[i].append(record)

def get_binomial(description):
    words = description.split("_")
    return words[0] + "_" + words[1]

num_old_records = []
num_new_records = []
for records in gene_records:
    num_old_records.append(len(records))
    num_new_records.append(0)

for i in range(4):
    for new_record in SeqIO.parse(open(new_alignments[i], "rU"), "fasta"):
        new_binomial = get_binomial(new_record.id)
        found = False
        for record in gene_records[i]:
            old_binomial = get_binomial(record.id)
            if old_binomial == new_binomial:
                found = True
                break
        if not found:
            gene_records[i].append(new_record)
            num_new_records[i] += 1

for i in range(4):
    print("gene,old num records,newly found records,current num records")
    print(gene_labels[i] + "," + str(num_old_records[i]) + "," + str(num_new_records[i]) + "," + str(len(gene_records[i])))
    SeqIO.write(gene_records[i], open(gene_labels[i] + "_final.fasta","w"), "fasta")

