library(tm)
library(dplyr)
library(lubridate)
library(stm) # Structural Topic Model

# stop words --------------------------------------------------------------


Mystopwords <- c("ainda", "ante", "p", "r", "sobre", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "meses", "ano", "anos", as.character(0:9), as.character(1990:2023), tm::stopwords("pt"))
Mystopwords <- c(Mystopwords, "inflação", "preço", "preços", "taxa", "comitê", "copom", "anterior", "política", "monetária", "economia", "relação", "doze", "membro", "cenário")
# loading corpus ----------------------------------------------------------

listAtas <- list.files(path = "../atas", pattern = ".txt", all.files = TRUE, full.names = TRUE)

print(paste(length(listAtas), "atas"))

listText <- c()
for (ata in listAtas) {
  lines <- readLines(con = ata, encoding = "UTF-8")
  lines <- paste(lines, collapse = " ")
  listText <- c(listText, lines)
}
print(paste(length(listText), "atas"))

df <- read.csv2("../decisions.csv", sep = ",")
df[df$meeting == 45 & df$decision == "keep", "meeting"] <- NA
df <- df %>% na.omit()
df <- df %>% arrange(meeting)

df$text <- listText
colnames(df) <- c("doc_id", "selic", "decision", "text")

df_aux <- read.csv2("../copom_dates.csv", sep = ",")

df$date <- as.Date(df_aux$publish_date) # df_aux is already sorted
df$selic <- as.numeric(df$selic)
rm(df_aux)

# pre-processing ----------------------------------------------------------

docs <- Corpus(DataframeSource(df))
toSpace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "\n")
docs <- tm_map(docs, toSpace, "\r")
docs <- tm_map(docs, toSpace, "\t")
docs <- tm_map(docs, toSpace, "_")
docs <- tm_map(docs, toSpace, "-")
docs <- tm_map(docs, toSpace, "\\(")
docs <- tm_map(docs, toSpace, "\\)")
docs <- tm_map(docs, toSpace, "'")
docs <- tm_map(docs, toSpace, '"')
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, removePunctuation)
docs <- tm_map(docs, removeWords, Mystopwords)
docs <- tm_map(docs, stripWhitespace)

df$text_clean <- docs$content

# Ingest ------------------------------------------------------------------


processed <- textProcessor(df$text_clean, metadata = df[, c("doc_id", "selic", "decision", "date")])
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta

# Prepare -----------------------------------------------------------------

plotRemoved(processed$documents, lower.thresh = seq(1, 200, by = 100))
out <- prepDocuments(processed$documents, processed$vocab, processed$meta, lower.thresh = 15)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta

# Estimate ----------------------------------------------------------------

model <- stm(documents = out$documents, vocab = out$vocab, K = 20, prevalence = ~ doc_id + selic + decision + year(date), max.em.its = 75, data = out$meta, init.type = "Spectral")


# Understand --------------------------------------------------------------


print(labelTopics(model))

thoughts6 <- findThoughts(model, texts = df$text, n = 1, topics = 6)$docs[[1]]
thoughts18 <- findThoughts(model, texts = df$text, n = 1, topics = 18)$docs[[1]]
par(mfrow = c(1, 2), mar = c(0.5, 0.5, 1, 0.5))
plotQuote(thoughts6, width = 30, main = "Topic 6")
plotQuote(thoughts18, width = 30, main = "Topic 18")

prep <- estimateEffect(~ doc_id + selic + decision + year(date), model, meta = out$meta, uncertainty = "Global")
print(summary(prep))
# summary(prep, topics = 1)
# summary(prep, topics = 2)


# Visualize ---------------------------------------------------------------

plot(model, type = "summary", xlim = c(0, 0.3))
