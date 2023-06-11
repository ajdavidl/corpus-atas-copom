library(dplyr)
library(tm)
library(topicmodels)

print("Loading data...")
listAtas <- list.files(path = "../atas", pattern = ".txt", all.files = TRUE, full.names = TRUE)
print(paste(length(listAtas), "atas"))

corpus <- c()
for (ata in listAtas) {
    lines <- readLines(con = ata, encoding = "UTF-8")
    lines <- paste(lines, collapse = " ")
    corpus <- c(corpus, lines)
}
print(paste(length(corpus), "atas"))

doc_ids <- seq(21, 21 + length(listAtas) - 1, 1)
df <- data.frame(doc_id = doc_ids, text = corpus, stringsAsFactors = FALSE)

Mystopwords <- c("ainda", "ante", "p", "r", "sobre", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "meses", "ano", "anos", as.character(0:9), tm::stopwords("pt"))
Mystopwords <- c(Mystopwords, "inflação", "preços", "preço", "doze", "meses", "segundo", "copom", "monetária", "política", "economia", "taxa", "dia", "volátil", "após", "desde", "quanto", "assim", "reunião", "relação", "mensal", "meses", "trimestre", "maior", "dia", "respectivamente")
print("Preparing data...")
docs <- Corpus(DataframeSource(df))
# Transform to lower case
docs <- tm_map(docs, content_transformer(tolower))
# remove potentially problematic symbols
toSpace <- content_transformer(function(x, pattern) {
    return(gsub(pattern, " ", x))
})
docs <- tm_map(docs, toSpace, "-")
# remove punctuation
docs <- tm_map(docs, removePunctuation)
# Strip digits
docs <- tm_map(docs, removeNumbers)
# remove stopwords
docs <- tm_map(docs, removeWords, Mystopwords)
# remove whitespace
docs <- tm_map(docs, stripWhitespace)
# Create document-term matrix
dtm <- DocumentTermMatrix(docs)

print("Running LDA...")
# Run LDA using Gibbs sampling
ldaOut <- LDA(dtm,
    k = 10,
    method = "Gibbs",
    control = list(
        nstart = 3,
        seed = list(2003, 5, 63),
        best = TRUE,
        burnin = 4000,
        iter = 2000,
        thin = 500
    )
)
# write out results
# docs to topics
ldaOut.topics <- as.matrix(topics(ldaOut))
colnames(ldaOut.topics) <- "Tópico"
# top 6 terms in each topic
ldaOut.terms <- as.matrix(terms(ldaOut, 20))
# probabilities associated with each topic assignment
topicProbabilities <- as.data.frame(ldaOut@gamma)
row.names(topicProbabilities) <- row.names(ldaOut.topics)


knitr::kable(ldaOut.terms, digits = 2, caption = "Terms in topics")
knitr::kable(ldaOut.topics, digits = 2, caption = "Topics of each minute")
knitr::kable(topicProbabilities, digits = 2, caption = "Probabilities of Topics")
