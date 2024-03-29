library(dplyr)
library(tidytext)
library(tidyr)
source("load_texts.R")

corpus <- read_text_files()

print(paste(length(corpus),"atas"))

df <- data.frame(sentence = corpus, stringsAsFactors = FALSE)

charFreq <- df %>%
  unnest_tokens(character, sentence, token = "characters") %>%
  count(character, sort = TRUE) %>%
  ungroup()
print(charFreq[1:20,])

charFreq2 <- df %>%
  unnest_tokens(character, sentence, token = "character_shingles", n=2) %>%
  count(character, sort = TRUE) %>%
  ungroup()
print(charFreq2[1:20,])

charFreq3 <- df %>%
  unnest_tokens(character, sentence, token = "character_shingles", n=3) %>%
  count(character, sort = TRUE) %>%
  ungroup()
print(charFreq3[1:20,])

charFreq4 <- df %>%
  unnest_tokens(character, sentence, token = "character_shingles", n=4) %>%
  count(character, sort = TRUE) %>%
  ungroup()
print(charFreq4[1:20,])
