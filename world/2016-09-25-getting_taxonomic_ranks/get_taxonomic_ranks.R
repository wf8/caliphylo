
library(taxize)

testing = FALSE
taxids = read.csv("taxids.csv", header=FALSE, stringsAsFactors=FALSE)
num_rows = nrow(taxids)

data_out = data.frame(genus = character(),
                      family = character(),
                      order = character(),
                      class = character(),
                      clade = character(),
                      stringsAsFactors=FALSE) 

for (i in 1:num_rows) {

    if (taxids[i, 2] != "not found") {
        
        ranks = classification(taxids[i, 2], db='ncbi')[[1]]
        num_ranks = nrow(ranks)
        
        if (num_ranks > 0) {
            genus = ""
            family = ""
            order = ""
            class = ""
            clade = ranks$name[9]

            for (j in 1:num_ranks) {
                
                if (ranks$rank[j] == "class" || ranks$rank[j] == "subclass")
                    class = ranks$name[j]
                if (ranks$rank[j] == "order")
                    order = ranks$name[j]
                if (ranks$rank[j] == "family")
                    family = ranks$name[j]
                if (ranks$rank[j] == "genus")
                    genus = ranks$name[j]

            }

            new_row = data.frame(genus = genus, 
                                 family = family,
                                 order = order,
                                 class = class,
                                 clade = clade)
            data_out = rbind(data_out, new_row)
        }
    }

    if (testing && i == 3)
        break
}

write.csv(data_out, file = "taxonomic_ranks.csv", row.names = FALSE, quote = FALSE)
