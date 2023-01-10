library(textplot)
library(udpipe)
library(dplyr)
library(tidytext)


# stop words --------------------------------------------------------------


Mystopwords <- c("ainda", "ante", "p", "r", "sobre", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "meses", "ano", "anos", as.character(0:9), as.character(1990:2023), tm::stopwords("pt"))

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

# word frequency ----------------------------------------------------------


wordsFreq <- df %>%
  unnest_tokens(word, text) %>%
  filter(!word %in% Mystopwords) %>%
  count(word, sort = TRUE) %>%
  ungroup()

NrWords <- 20
mostFrequentWords <- wordsFreq$n[1:NrWords]
names(mostFrequentWords) <- wordsFreq$word[1:NrWords]
mostFrequentWords <- sort(mostFrequentWords)

textplot_bar(mostFrequentWords, panel = "Frequent words", total = sum(wordsFreq$n), col.panel = "darkgrey", xlab = "Listings", cextext = 0.75, addpct = TRUE, cexpct = 0.5)

# Word similarity chart ---------------------------------------------------

wordsFreq <- df %>%
  group_by(doc_id) %>%
  unnest_tokens(word, text) %>%
  filter(!word %in% Mystopwords) %>%
  count(word, sort = TRUE) %>%
  ungroup()

colnames(wordsFreq) <- c("doc_id", "term", "freq")

dtm <- document_term_matrix(wordsFreq)
dtm <- dtm_remove_lowfreq(dtm, maxterms = 30)
# dtm

m <- dtm_cor(dtm)
textplot_correlation_glasso(m, exclude_zero = TRUE)

# Dependency Parsing ------------------------------------------------------


sentences <- tokenizers::tokenize_sentences(df$text[length(df$text)])

sent <- udpipe(sentences[[1]][length(sentences[[1]])], "portuguese")

textplot_dependencyparser(sent)

# Word Cooccurrence Graph -------------------------------------------------

sentences <- tokenizers::tokenize_sentences(listText, lowercase = TRUE)
listSentences <- c()
for (i in 1:length(sentences)) {
  listSentences <- c(listSentences, sentences[[i]])
}

dfSentences <- data.frame(doc_id = 1:length(listSentences), text = listSentences)

wordsFreq <- dfSentences %>%
  group_by(doc_id) %>%
  unnest_tokens(word, text) %>%
  filter(!word %in% Mystopwords) %>%
  count(word, sort = TRUE) %>%
  ungroup()

cooc <- cooccurrence(wordsFreq, group = "doc_id", term = "word")
cooc$cooc <- cooc$cooc / 1000
textplot_cooccurrence(cooc, top_n = 25)
