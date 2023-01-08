library(text2vec)
library(tm)

listAtas <- list.files(path = "../atas", pattern = ".txt", all.files = TRUE, full.names = TRUE)

print(paste(length(listAtas), "atas"))

corpus <- c()
for (ata in listAtas) {
  lines <- readLines(con = ata, encoding = "UTF-8")
  lines <- paste(lines, collapse = " ")
  corpus <- c(corpus, lines)
}

corpus <- tolower(corpus)

Mystopwords <- c("ainda", "ante", "p", "r", "sobre", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "meses", "ano", "anos", as.character(0:9), tm::stopwords("pt"))

it <- itoken(corpus)
model <- Collocations$new(collocation_count_min = 10)
model$fit(it, n_iter = 10)

df <- model$collocation_stat
print(df[1:20, c("prefix", "suffix")])

# -------------------------------------------------------------------------


it <- itoken(corpus)
v <- create_vocabulary(it, stopwords = Mystopwords)
v <- prune_vocabulary(v, term_count_min = 50)
model2 <- Collocations$new(vocabulary = v, collocation_count_min = 50, pmi_min = 0)
model2$partial_fit(it)
model2$fit(it, n_iter = 10)

df2 <- model2$collocation_stat
print(df2[1:20, c("prefix", "suffix")])
