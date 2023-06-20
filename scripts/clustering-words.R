library(dplyr)
library(tm)
library(topicmodels)
library(cluster) # Hierarchal Clustering
library(fpc) # K-means clustering
library(ape)

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

dtmss <- removeSparseTerms(dtm, 0.1)

dtmss <- as.matrix(dtmss)

print("Running clustering of words...")
# Hierarchal Clustering
d <- dist(t(dtmss), method = "euclidean")
fit <- hclust(d = d, method = "ward.D")
# Helping to Read a Dendrogram
plot(fit, hang = -1, main = "Hierarchal Cluster - Dendogram - Words")
plot(as.dendrogram(fit), hang = -1, horiz = TRUE, main = "Hierarchal Cluster - Dendogram - Words")
plot(as.phylo(fit), type = "fan", main = "Hierarchal Cluster - Words") # circular dendogram

# K-means clustering
d <- dist(t(dtmss), method = "euclidean")
kfit <- kmeans(d, 4)
clusplot(as.matrix(d), kfit$cluster, color = T, shade = T, labels = 2, lines = 0, main = "Kmeans Cluster - palavras - Todas as normas")
