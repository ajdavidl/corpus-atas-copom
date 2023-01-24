library(dplyr)
library(textreuse)

# stop words --------------------------------------------------------------


Mystopwords <- c('ainda','ante','p','r','sobre', 'janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro','mês','meses','ano','anos', as.character(0:9), as.character(1990:2023), tm::stopwords('pt'))

# loading corpus ----------------------------------------------------------

listAtas <- list.files(path="../atas", pattern=".txt", all.files=TRUE, full.names=TRUE)

print(paste(length(listAtas),"minutes"))

corpus <- c()
for(ata in listAtas){
  lines <- readLines(con = ata, encoding = "UTF-8")
  lines <- paste(lines, collapse = " ")
  corpus <- c(corpus,lines)
}
print(paste(length(corpus),"minutes"))

docNames <- substr(listAtas,12,14)

# jaccard_similarity --------------------------------------------------------------

ats_minhash <- minhash_generator(n = 100, seed = 923)
names(corpus) <- docNames
ats <- TextReuseCorpus(text = corpus,
                       tokenizer = tokenize_ngrams, n = 7, 
                       minhash_func = ats_minhash)
buckets <- lsh(ats, bands = 25)
ats_matches <- buckets %>% 
  lsh_candidates() %>% 
  lsh_compare(ats, jaccard_similarity)
ats_matches <- ats_matches %>% arrange(desc(score))

knitr::kable(ats_matches[1:30,], caption = 'Minutes - Jaccard similarity')


df<-data.frame(a = docNames[(length(docNames)-9):length(docNames)],
               b = docNames[(length(docNames)-10):(length(docNames)-1)],
               score = rep(NA,10),
               stringsAsFactors = FALSE)
aux<-lsh_compare(df, ats, jaccard_similarity)
knitr::kable(aux, caption = 'Similarity index - Jaccard Similarity')

df<-data.frame(a = docNames[(length(docNames)-10):(length(docNames)-1)],
               b = rep(docNames[length(docNames)], 10),
               score = rep(NA, 10),
               stringsAsFactors = FALSE)
aux<-lsh_compare(df, ats, jaccard_similarity)
knitr::kable(aux, caption = 'Similarity index - Jaccard Similarity')


# ratio_of_matches --------------------------------------------------------

# ratio of matches
df<-data.frame(a = docNames[(length(docNames)-9):length(docNames)],
               b = docNames[(length(docNames)-10):(length(docNames)-1)],
               score = rep(NA,10),
               stringsAsFactors = FALSE)
aux<-lsh_compare(df, ats, ratio_of_matches)
knitr::kable(aux, caption = 'Ratio of matches')


df<-data.frame(a = docNames[(length(docNames)-10):(length(docNames)-1)],
               b = rep(docNames[length(docNames)], 10),
               score = rep(NA, 10),
               stringsAsFactors = FALSE)
aux<-lsh_compare(df, ats, ratio_of_matches)
knitr::kable(aux, caption = 'Ratio of matches')

# jaccard_bag_similarity --------------------------------------------------

df<-data.frame(a = docNames[(length(docNames)-9):length(docNames)],
               b = docNames[(length(docNames)-10):(length(docNames)-1)],
               score = rep(NA,10),
               stringsAsFactors = FALSE)
aux<-lsh_compare(df, ats, jaccard_bag_similarity)
knitr::kable(aux, caption = 'jaccard bag similarity')

df<-data.frame(a = docNames[(length(docNames)-10):(length(docNames)-1)],
               b = rep(docNames[length(docNames)], 10),
               score = rep(NA, 10),
               stringsAsFactors = FALSE)
aux<-lsh_compare(df, ats, jaccard_bag_similarity)
knitr::kable(aux, caption = 'jaccard bag similarity')

