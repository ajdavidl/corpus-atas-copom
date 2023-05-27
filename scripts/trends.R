library(lubridate)
library(dplyr)
library(tidytext)
library(tokenizers)
library(tidyr)
library(tm)
library(ggplot2)
library(scales)
library(pracma)

# Mystopwords <- c("ainda", "ante", "p", "r", "sobre", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "meses", "ano", "anos", as.character(0:9), as.character(1990:2023), tm::stopwords("pt"))
# Mystopwords <- c(Mystopwords, "inflação", "preço", "preços", "taxa", "comitê", "copom", "anterior", "política", "monetária", "economia", "relação", "doze", "membro", "cenário")

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
colnames(df) <- c("meeting", "selic", "decision", "text")
df$selic <- NULL

df2 <- read.csv2("../copom_dates.csv", sep = ",", stringsAsFactors = FALSE)
colnames(df2) <- c("meeting", "begin_date", "end_date", "publish_date")
df2$begin_date <- NULL
df2$end_date <- NULL

df <- df %>% left_join(df2, by = "meeting")

rm(df2)

dim(df)[1]

for (i in 1:dim(df)[1]) {
  # UNIGRAMS ---------------------------------------------------------------

  unigrams <- data.frame(text = df$text[i])
  # remove numbers
  unigrams$text <- gsub("[[:digit:]]+", " ", unigrams$text)
  unigrams$text <- gsub("º", " ", unigrams$text)
  unigrams$text <- gsub("ª", " ", unigrams$text)
  # transform in tidy dataset one-token-per-row format
  unigrams <- unigrams %>% unnest_tokens(word, text, to_lower = TRUE)
  # remove stop words
  # unigrams<-unigrams %>% filter(!word %in% Mystopwords)
  # word frequency
  unigrams <- unigrams %>% count(word, sort = TRUE)


  # bigrams ----------------------------------------------------------------

  bigrams <- data.frame(text = df$text[i])
  bigrams$text <- gsub("[[:digit:]]+", " ", bigrams$text)
  bigrams$text <- gsub("º", " ", bigrams$text)
  bigrams$text <- gsub("ª", " ", bigrams$text)

  bigrams <- bigrams %>%
    unnest_tokens(bigram, text, token = "ngrams", n = 2, to_lower = TRUE)
  bigrams <- bigrams %>%
    count(bigram, sort = TRUE)

  # trigrams ---------------------------------------------------------------

  trigrams <- data.frame(text = df$text[i])
  trigrams$text <- gsub("[[:digit:]]+", " ", trigrams$text)
  trigrams$text <- gsub("º", " ", trigrams$text)
  trigrams$text <- gsub("ª", " ", trigrams$text)

  trigrams <- trigrams %>%
    unnest_tokens(trigram, text, token = "ngrams", n = 3, to_lower = TRUE)
  trigrams <- trigrams %>%
    count(trigram, sort = TRUE)


  aux <- data.frame(
    date = rep(
      as.Date(df$publish_date[i], format = "%Y-%m-%d"),
      length(unigrams$word) + length(bigrams$bigram) + length(trigrams$trigram)
    ),
    token = c(unigrams$word, bigrams$bigram, trigrams$trigram),
    n = c(unigrams$n, bigrams$n, trigrams$n),
    stringsAsFactors = FALSE
  )

  if (i == 1) {
    df_trend <- aux
  } else {
    df_trend <- rbind.data.frame(df_trend, aux)
  }
}

rm(unigrams, bigrams, trigrams)

# Plots -------------------------------------------------------------------

aux <- df_trend %>%
  group_by(date) %>%
  summarise(total = sum(n))

ggplot(aux, aes(x = date, y = total)) +
  geom_line() +
  ggtitle("Total de palavras por dia") +
  ylab("Nr ocorrências") +
  geom_smooth(method = "loess") +
  theme_bw()
df_Nr_Words_per_day <- aux
rm(aux)

trends <- function(words, date_min = as.Date("1998-01-01", format = "%Y-%m-%d")) {
  aux <- df_trend %>%
    filter(token %in% words) %>%
    select(date, n)
  aux <- aux %>% filter(date > date_min)
  aux <- aux %>%
    group_by(date) %>%
    summarise(tot = sum(n))

  aux <- aux %>% left_join(df_Nr_Words_per_day, by = "date")
  aux$tot <- aux$tot / aux$total * 100

  ggplot(aux, aes(x = date, y = tot)) +
    geom_line() +
    ggtitle(words[1]) +
    ylab("%") +
    geom_smooth(method = "loess") +
    theme_bw() +
    scale_x_date(labels = date_format("%m-%Y"), date_breaks = "6 months") +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))
}

trends("inflação")
trends("preços")
trends(c("câmbio", "dólar"))
trends(c("pib", "atividade"))
trends("incerteza")
trends("guerra")
trends(c("selic", "juros"))
trends("taxa de juros")
trends(c("covid", "coronavírus", "pandemia"))
trends("preços administrados")
trends("livres")
trends("fiscal")
trends("política monetária")
trends("hiato")
