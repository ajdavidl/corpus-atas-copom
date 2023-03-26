library(text2vec)
library(dplyr)

listAtas <- list.files(path = "../atas", pattern = ".txt", all.files = TRUE, full.names = TRUE)

print(paste(length(listAtas), "atas"))

corpus <- c()
for (ata in listAtas) {
    lines <- readLines(con = ata, encoding = "UTF-8")
    lines <- paste(lines, collapse = " ")
    corpus <- c(corpus, lines)
}

corpus <- tolower(corpus)

Mystopwords <- c("ainda", "ante", "p", "r", "sobre", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "meses", "ano", "anos", as.character(0:9), tm::stopwords("pt"))

Vector_size <- 100
Nr_epochs <- 100

words <- tokenizers::tokenize_words(corpus)

it <- itoken(words, progressbar = FALSE, preprocess_function = tolower)
vocab <- create_vocabulary(it)

vectorizer <- vocab_vectorizer(vocab)
tcm <- create_tcm(it, vectorizer, skip_grams_window = 5L)

model_glove <- GlobalVectors$new(word_vectors_size = Vector_size, vocabulary = vocab, x_max = 100)

word_vectors_main <- model_glove$fit_transform(tcm, n_iter = Nr_epochs)
word_vectors_context <- model_glove$components
word_vectors <- word_vectors_main + t(word_vectors_context)

print(dim(word_vectors))

df <- data.frame(
    word = row.names(word_vectors),
    word_vectors,
    stringsAsFactors = FALSE
)
row.names(df) <- NULL

df2 <- df %>% filter(word %in% c(
    "inflação", "ipca", "juros", "selic", "câmbio", "dólar", "pib", "atividade", "hiato"
))


points <- df2[2:ncol(df2)]
row.names(points) <- df2[, 1]

fit <- cmdscale(dist(points), eig = TRUE, k = 2)
x <- fit$points[, 1]
y <- fit$points[, 2]

plot(x, y, pch = 19, xlab = "Coordinate 1", ylab = "Coordinate 2", main = "words Based on Global vectors algorithm", type = "n")
text(x, y, labels = row.names(points), cex = .7)

vector <- word_vectors["ipca", , drop = FALSE] - word_vectors["inflação", , drop = FALSE] +
    word_vectors["selic", , drop = FALSE]
cos_sim <- sim2(x = word_vectors, y = vector, method = "cosine", norm = "l2")
head(sort(cos_sim[, 1], decreasing = TRUE), 5)
