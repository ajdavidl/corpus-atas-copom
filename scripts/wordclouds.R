library(dplyr)
library(tidytext)
library(tidyr)
library(tm)
library(wordcloud)

source("load_texts.R")

numberOfWords <- 20

df <-return_data_frame()

wordsFreq <- df %>%
    unnest_tokens(word, text) %>%
    count(word, sort = TRUE) %>%
    ungroup()

wordsFreq <- wordsFreq %>%
    filter(!word %in% Mystopwords)
print(wordsFreq[1:numberOfWords, ])

wordcloud(
    words = wordsFreq$word, freq = wordsFreq$n, min.freq = 1000,
    random.order = FALSE, max.words = 1000, rot.per = 0,
    colors = brewer.pal(6, "Dark2"), scale = c(4, 0.8)
)

Mystopwords <- c(Mystopwords, "inflação", "preços", "taxa", "copom", "bilhões", "crescimento",
                 "bens","produção", "cenário", "política", "monetária", "período", "anterior",
                 "us","p.p","índice","mercado","comitê","atividade", "acordo", "mensal", "leva",
                 "janeiro","fevereiro","março","abril","maio","junho","julho","agosto",
                 "setembro","outubro","novembro","dezembro","econômica","economia","mês",
                 "taxas", "vista", "_","-","reunião","bem","relação","primeiro","segundo",
                 "terceiro","quarto","luiz","tal","dia","paulo","diz","vem")

df2 <- df[,c("meeting","text","decision")]
colnames(df2) <- c("doc_id","text","decision")
lower <- df2[df2$decision == "lower",]
raise <- df2[df2$decision == "raise",]
keep <- df2[df2$decision == "keep",]

lower <- as.vector(lower$text)
raise <- as.vector(raise$text)
keep <- as.vector(keep$text)

All <- list(lower, raise, keep)

docs <- Corpus(VectorSource(All))
toSpace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, removePunctuation)
docs <- tm_map(docs, removeWords, Mystopwords)
docs <- tm_map(docs, stripWhitespace)

tdm <- TermDocumentMatrix(docs)
tdm = removeSparseTerms(tdm, 0.98)
tdm = as.matrix(tdm)
colnames(tdm) <- c("redução", "aumento", "manutenção")

comparison.cloud(tdm, max.words = 500, random.order = FALSE, rot.per = 0, scale = c(2, 0.5), fixed.asp=T, title.size = 1)
commonality.cloud(tdm, max.words = 300, random.order = FALSE, rot.per = 0, scale = c(2, 0.5))
