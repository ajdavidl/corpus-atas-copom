library(dplyr)
library(tidytext)
library(tidyr)
library(ggplot2)
library(scales)
source("load_texts.R", encoding = "UTF-8")

# loading corpus ----------------------------------------------------------
print("Loading files ...")
df <-return_data_frame()
print(paste(as.character(dim(df)[1]), "atas"))

print("Counting ngrams ...")
for (i in 1:dim(df)[1]) {
  # UNIGRAMS ---------------------------------------------------------------

  unigrams <- data.frame(text = df$text[i])
  # remove numbers
  unigrams$text <- gsub("[[:digit:]]+", " ", unigrams$text)
  unigrams$text <- gsub("º", " ", unigrams$text)
  unigrams$text <- gsub("ª", " ", unigrams$text)
  # transform in tidy dataset one-token-per-row format
  unigrams <- unigrams %>% unnest_tokens(word, text, to_lower = TRUE) %>% 
    count(word, sort = TRUE)


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
print("Plotting ...")

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
trends(c("preço","preços"))
trends(c("câmbio", "dólar"))
trends(c("pib", "atividade"))
trends("incerteza")
trends("guerra")
trends(c("selic", "juros"))
trends("taxa de juros")
trends(c("covid", "coronavírus", "pandemia"), date_min = as.Date("2020-01-01"))
trends("preços administrados")
trends("livres")
trends(c("fiscal","dívida líquida","dívida bruta","superávit primário"))
trends("política monetária")
trends("hiato")
trends(c("risco","riscos"))
trends(c("energia","bandeira","bandeiras","energética","energético"))
trends(c("focus","expectativa","expectativas"))
