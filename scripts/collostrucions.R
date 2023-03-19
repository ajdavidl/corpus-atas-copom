library(dplyr)
library(tidytext)
library(tokenizers)
library(tidyr)

# collostrucion package ---------------------------------------------------

# The package is available in the link:
# https://sfla.ch/collostructions/
# Install it with the command:
# > install.packages(file.choose(), repos = NULL)
# select the package file

library(collostructions)

# loading corpus ----------------------------------------------------------

listAtas <- list.files(path = "../atas", pattern = ".txt", all.files = TRUE, full.names = TRUE)

print(paste(length(listAtas), "minutes"))

corpus <- c()
for (ata in listAtas) {
    lines <- readLines(con = ata, encoding = "UTF-8")
    lines <- paste(lines, collapse = " ")
    corpus <- c(corpus, lines)
}

print(paste(length(corpus), "minutes"))

docNames <- substr(listAtas, 12, 14)

df <- data.frame(doc_id = docNames, text = corpus)

# Word frequency ----------------------------------------------------------

words_freq <- df %>%
    unnest_tokens(word, text) %>%
    count(word, sort = TRUE) %>%
    ungroup()
head(words_freq)

nr_words <- sum(words_freq$n)

# bigram frequency --------------------------------------------------------

bigram_freq <- df %>%
    unnest_tokens(word, text, token = "ngrams", n = 2) %>%
    count(word, sort = TRUE) %>%
    ungroup()

bigram_freq <- bigram_freq %>%
    select(word, n) %>%
    separate(word, c("word1", "word2"), sep = " ")

head(bigram_freq)

# trigram frequency -------------------------------------------------------

trigram_freq <- df %>%
    unnest_tokens(word, text, token = "ngrams", n = 3) %>%
    count(word, sort = TRUE) %>%
    ungroup()

trigram_freq <- trigram_freq %>%
    select(word, n) %>%
    separate(word, c("word1", "word2", "word3"), sep = " ")

# collostructional analysis -----------------------------------------------

collostruction_analysis <- function(word, df_word_freq, df_bigram_freq, corpus_size) {
    df_coll <- df_bigram_freq[df_bigram_freq$word1 == word, ]
    df_coll$word1 <- NULL
    df_coll <- merge(x = df_coll, y = df_word_freq, by.x = "word2", by.y = "word", all.x = TRUE)
    colnames(df_coll) <- c("WORD", "CXN_FREQ", "CORP_FREQ")
    return(collex(df_coll, nr_words))
}

collostruction_analysis2 <- function(word1, word2, df_word_freq, df_trigram_freq, corpus_size) {
    df_coll <- df_trigram_freq[df_trigram_freq$word1 == word1, ]
    df_coll <- df_coll[df_coll$word2 == word2, ]
    df_coll$word1 <- NULL
    df_coll$word2 <- NULL
    df_coll <- merge(x = df_coll, y = df_word_freq, by.x = "word3", by.y = "word", all.x = TRUE)
    colnames(df_coll) <- c("WORD", "CXN_FREQ", "CORP_FREQ")
    return(collex(df_coll, nr_words))
}

collostruction_analysis("inflação", words_freq, bigram_freq, nr_words)
collostruction_analysis("ipca", words_freq, bigram_freq, nr_words)
collostruction_analysis("juros", words_freq, bigram_freq, nr_words)
collostruction_analysis("selic", words_freq, bigram_freq, nr_words)
collostruction_analysis("câmbio", words_freq, bigram_freq, nr_words)
collostruction_analysis("dólar", words_freq, bigram_freq, nr_words)
collostruction_analysis("atividade", words_freq, bigram_freq, nr_words)
collostruction_analysis("pib", words_freq, bigram_freq, nr_words)

collostruction_analysis2("aumento", "de", words_freq, trigram_freq, nr_words)
collostruction_analysis2("redução", "de", words_freq, trigram_freq, nr_words)
collostruction_analysis2("banco", "central", words_freq, trigram_freq, nr_words)
collostruction_analysis2("preços", "administrados", words_freq, trigram_freq, nr_words)
collostruction_analysis2("preços", "livres", words_freq, trigram_freq, nr_words)
collostruction_analysis2("política", "monetária", words_freq, trigram_freq, nr_words)
