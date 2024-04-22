library(dplyr)
library(tidytext)
library(tokenizers)
library(tidyr)
library(ggplot2)
library(tm)
library(wordcloud)

source("load_texts.R", encoding = "UTF-8")

df <-return_data_frame()

numberOfWords <- 20

print("Word frequency with stop words")

wordsFreq <- df %>%
    unnest_tokens(word, text) %>%
    count(word, sort = TRUE) %>%
    ungroup()
print(wordsFreq[1:numberOfWords, ])

ggplot(wordsFreq[1:numberOfWords, ], aes(x = reorder(word, n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("words") +
    ggtitle("Word frequencies with stop words") +
    theme_bw() +
    theme(text = element_text(size = 20)) +
    coord_flip()

wordcloud(
    words = wordsFreq$word, freq = wordsFreq$n, min.freq = 1000,
    random.order = FALSE, max.words = 1000, rot.per = 0,
    colors = brewer.pal(6, "Dark2"), scale = c(5, 1.2)
)

print("Word frequency without stop words")

wordsFreq2 <- wordsFreq %>%
    filter(!word %in% Mystopwords)
print(wordsFreq2[1:numberOfWords, ])

ggplot(wordsFreq2[1:numberOfWords, ], aes(x = reorder(word, n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("words") +
    ggtitle("Word frequencies without stop words") +
    theme_bw() +
    theme(text = element_text(size = 20)) +
    coord_flip()

wordcloud(
    words = wordsFreq2$word, freq = wordsFreq2$n, min.freq = 1000,
    random.order = FALSE, max.words = 1000, rot.per = 0,
    colors = brewer.pal(6, "Dark2"), scale = c(4, 0.8)
)

print("Bigram frequency with stop words")

numberOfBigram <- 20

bigramFreq <- df %>%
    unnest_tokens(word, text, token = "ngrams", n = 2) %>%
    count(word, sort = TRUE) %>%
    ungroup()
print(bigramFreq[1:numberOfBigram, ])

ggplot(bigramFreq[1:numberOfBigram, ], aes(x = reorder(word, n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("bigrams") +
    ggtitle("Bigram frequencies with stop words") +
    theme_bw() +
    theme(text = element_text(size = 20)) +
    coord_flip()

wordcloud(
    words = bigramFreq$word, freq = bigramFreq$n, min.freq = 1000,
    random.order = FALSE, max.words = 1000, rot.per = 0,
    colors = brewer.pal(6, "Dark2"), scale = c(3.8, 0.6)
)


print("Bigram frequency without stop words")

bigramFreq2 <- bigramFreq %>%
    select(word, n) %>%
    separate(word, c("word1", "word2"), sep = " ")

bigramFreq2 <- bigramFreq2 %>%
    filter(!word1 %in% Mystopwords) %>%
    filter(!word2 %in% Mystopwords)

bigramFreq2 <- bigramFreq2 %>%
    select(word1, word2, n) %>%
    unite(word, word1, word2, sep = " ")
print(bigramFreq2[1:numberOfBigram, ])

ggplot(bigramFreq2[1:numberOfBigram, ], aes(x = reorder(word, n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("bigrams") +
    ggtitle("Bigram frequencies without stop words") +
    theme_bw() +
    theme(text = element_text(size = 20)) +
    coord_flip()

wordcloud(
    words = bigramFreq2$word, freq = bigramFreq2$n, min.freq = 200,
    random.order = FALSE, max.words = 500, rot.per = 0,
    colors = brewer.pal(6, "Dark2"), scale = c(3, 0.5)
)

print("Trigram frequency with stop words")

numberOfTrigram <- 20

trigramFreq <- df %>%
    unnest_tokens(word, text, token = "ngrams", n = 3) %>%
    count(word, sort = TRUE) %>%
    ungroup()
print(trigramFreq[1:numberOfTrigram, ])

ggplot(trigramFreq[1:numberOfTrigram, ], aes(x = reorder(word, n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("trigrams") +
    ggtitle("Trigram frequencies with stop words") +
    theme_bw() +
    theme(text = element_text(size = 20)) +
    coord_flip()

wordcloud(
    words = trigramFreq$word, freq = trigramFreq$n, min.freq = 100,
    random.order = FALSE, max.words = 250, rot.per = 0,
    colors = brewer.pal(6, "Dark2"), scale = c(2.5, 0.3)
)

print("Trigram frequency without stop words")

trigramFreq2 <- trigramFreq %>%
    select(word, n) %>%
    separate(word, c("word1", "word2", "word3"), sep = " ")

trigramFreq2 <- trigramFreq2 %>%
    filter(!word1 %in% Mystopwords) %>%
    filter(!word2 %in% Mystopwords) %>%
    filter(!word3 %in% Mystopwords)

trigramFreq2 <- trigramFreq2 %>%
    select(word1, word2, word3, n) %>%
    unite(word, word1, word2, word3, sep = " ")
print(trigramFreq2[1:numberOfTrigram, ])

ggplot(trigramFreq2[1:numberOfTrigram, ], aes(x = reorder(word, n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("trigrams") +
    ggtitle("Trigram frequencies without stop words") +
    theme_bw() +
    theme(text = element_text(size = 20)) +
    coord_flip()

wordcloud(
    words = trigramFreq2$word, freq = trigramFreq2$n, min.freq = 50,
    random.order = FALSE, max.words = 200, rot.per = 0,
    colors = brewer.pal(6, "Dark2"), scale = c(2.3, 0.3)
)
