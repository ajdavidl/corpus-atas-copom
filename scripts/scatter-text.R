library(tidytext)
library(dplyr)
library(readr)
library(tidyverse)
library(tm)
library(tidyr)
library(scales)
source("load_texts.R", encoding = "UTF-8")

# Adapted from https://gist.github.com/rll307/efc6cb331d570c3733c1abdee134b05a

df <-return_data_frame()
Mystopwords <- c(Mystopwords, "apresenta", "assim", "contra", "ter","b","c","d","f")

all <- df %>% select(decision, text) %>% 
  unnest_tokens(word, text) %>%
  count(word, sort = TRUE) %>% 
  filter(!word %in% Mystopwords)

lower <- df %>% select(decision, text) %>% 
  filter(decision == "lower") %>% 
  unnest_tokens(word, text) %>%
  count(word, sort = TRUE) %>% 
  filter(!word %in% Mystopwords)
  
keep <- df %>% select(decision, text) %>% 
  filter(decision == "keep") %>% 
  unnest_tokens(word, text) %>%
  count(word, sort = TRUE) %>% 
  filter(!word %in% Mystopwords)
  
raise <- df %>% select(decision, text) %>%
  filter(decision == "raise") %>% 
  unnest_tokens(word, text) %>%
  count(word, sort = TRUE) %>% 
  filter(!word %in% Mystopwords)

frequency <- bind_rows(mutate(raise, decision = "raise"),
                       mutate(keep, decision = "keep"),
                       mutate(lower, decision = "lower")) %>%
  mutate(word = str_extract(word, "[a-z']+")) %>%
  count(decision, word) %>%
  group_by(decision) %>%
  mutate(proportion = n / sum(n)) %>%
  select(-n) %>%
  spread(decision, proportion)

frequency <- frequency %>% filter(word %in% all$word[1:1000])

ggplot(frequency, aes(x = raise, y = lower, color = abs(raise - lower))) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) + 
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) + 
  scale_x_log10(labels = percent_format()) +
  scale_y_log10(labels = percent_format()) + 
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") + 
  labs(y = "Lower", x = "Raise", title = "Raise X Lower")


ggplot(frequency, aes(x = raise, y = keep, color = abs(raise - keep))) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) + 
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) + 
  scale_x_log10(labels = percent_format()) +
  scale_y_log10(labels = percent_format()) + 
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") + 
  labs(y = "Keep", x = "Raise", title = "Raise X Keep")


ggplot(frequency, aes(x = keep, y = lower, color = abs(keep - lower))) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) + 
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) + 
  scale_x_log10(labels = percent_format()) +
  scale_y_log10(labels = percent_format()) + 
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") + 
  labs(y = "Lower", x = "Keep", title = "Keep X Lower")
