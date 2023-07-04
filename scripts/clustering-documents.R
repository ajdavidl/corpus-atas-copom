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

dtm_tfxidf <- weightTfIdf(dtm)
### k-means (this uses euclidean distance)
m <- as.matrix(dtm_tfxidf)
rownames(m) <- as.character(df$doc_id)
### normalize the vectors so Euclidean makes sense
norm_eucl <- function(m) m/apply(m, MARGIN=1, FUN=function(x) sum(x^2)^.5)
m_norm <- norm_eucl(m)
### cluster into 10 clusters
cl <- kmeans(m_norm, 10)
### show clusters using the first 2 principal components
plot(prcomp(m_norm)$x, col=cl$cl)

print("Clustering documents...") 
d <- dist(m, method="euclidean")
hc <- hclust(d, method="average")
#plot dendogram divided
hcd <- as.dendrogram(hc)
par(cex=0.7, mar=c(5, 8, 4, 1))
plot(hcd, main = "Hierarchical Cluster - dendogram")
plot(hcd, horiz = TRUE, main = "Hierarchical Cluster - dendogram")
plot(as.phylo(hc), type = "fan",main = "Hierarchical Cluster - circular dendogram") #dendogram circular
