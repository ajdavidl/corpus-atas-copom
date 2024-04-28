library(udpipe)
library(dplyr)
library(ggplot2)
library(scales)
source("load_texts.R", encoding = "UTF-8")

# loading corpus ----------------------------------------------------------
print("Loading files ...")
df <-return_data_frame()
print(paste(as.character(dim(df)[1]), "atas"))
corpus <- df$text

# udpipe_download_model("portuguese-bosque")
model <- udpipe_load_model(file = "portuguese-bosque-ud-2.5-191206.udpipe")

parse <- function(txt) {
    if (Encoding(txt) != "unknown") txt <- iconv(txt, from = Encoding(txt), to = "UTF-8")
    y <- udpipe_annotate(model, x = txt)
    # cat(y$conllu)
    con <- textConnection(y$conllu)
    tabela <- read.table(con, sep = "\t", skip = 4, fill = TRUE, fileEncoding = "UTF-8", header = FALSE, comment.char = "", check.names = FALSE, stringsAsFactors = FALSE)
    df <- as.data.frame(tabela)
    df <- df %>% filter(!grepl("# sent_id", V1) & !grepl("# text", V1))
    names(df) <- c("ID", "FORM", "LEMMA", "UPOSTAG", "XPOSTAG", "FEATS", "HEAD", "DEPREL", "DEPS", "MISC")
    df <- df[, c(1, 2, 4, 7, 8)]
    close(con)
    return(df)
}

formality <- function(df_parsed){
    # df_parsed is the return of parse function
    tags <- df_parsed$UPOSTAG
    NOUN <- sum(tags == "NOUN")
    PROPN <- sum(tags == "PROPN")
    ADJ <- sum(tags == "ADJ")
    DET <- sum(tags == "DET")
    PRON <- sum(tags == "PRON")
    ADV <- sum(tags == "ADV")
    VERB <- sum(tags == "VERB")
    AUX <- sum(tags == "AUX")
    INTJ <- sum(tags == "INTJ")
    CONJ <- sum(tags == "CONJ")
    CCONJ <- sum(tags == "CCONJ")
    SCONJ <- sum(tags == "SCONJ")
    F = NOUN + PROPN + ADJ + DET
    C = PRON + ADV + VERB + AUX + INTJ
    N = F + C + CONJ + CCONJ + SCONJ
    if (N == 0) return(0)
    else {
        formality = 50 * ((F - C)/N + 1)
        return(formality)
    }
}

lexical_density <- function(df_parsed){
    # df_parsed is the return of parse function
    tags <- df_parsed$UPOSTAG
    NOUN <- sum(tags == "NOUN")
    PROPN <- sum(tags == "PROPN")
    ADJ <- sum(tags == "ADJ")
    ADP <- sum(tags == "ADP")
    DET <- sum(tags == "DET")
    PRON <- sum(tags == "PRON")
    ADV <- sum(tags == "ADV")
    VERB <- sum(tags == "VERB")
    AUX <- sum(tags == "AUX")
    INTJ <- sum(tags == "INTJ")
    CONJ <- sum(tags == "CONJ")
    CCONJ <- sum(tags == "CCONJ")
    SCONJ <- sum(tags == "SCONJ")
    NUM <- sum(tags == "NUM")
    PART <- sum(tags == "PART")
    N = ADJ + ADP + ADV + AUX + CONJ + CCONJ + DET + INTJ + NOUN + NUM + PART + PRON + PROPN + SCONJ + VERB
    if (N == 0) return(0)
    else{
        lex_den = (NOUN + PROPN + ADJ + ADV + VERB + AUX)/N
        return(lex_den)
    }
}

Nr_docs <- length(corpus)
# cria lista de matrizes com o resultado do parse
lista_parse <- vector("list", Nr_docs)
formality_ <- vector("list", Nr_docs)
lexical_density_ <- vector("list", Nr_docs)

print("parsing ...")
for (i in 1:Nr_docs) {
    corpus[i] <- stringr::str_replace(pattern = "\"", replacement = " ", string = corpus[i])
    corpus[i] <- stringr::str_replace(pattern = "'", replacement = " ", string = corpus[i])
    corpus[i] <- stringr::str_replace(pattern = "\"", replacement = " ", string = corpus[i])
    corpus[i] <- stringr::str_replace(pattern = "'", replacement = " ", string = corpus[i])
    corpus[i] <- stringr::str_replace(pattern = "%", replacement = " ", string = corpus[i])
    lista_parse[[i]] <- parse(txt = corpus[i])
    formality_[[i]] <- formality(lista_parse[[i]])
    lexical_density_[[i]] <- lexical_density(lista_parse[[i]])
    if (i %% 25 == 0) print(paste(as.character(i),"documents parsed."))
}

matriz_parse <- lista_parse[[1]]
for (i in 2:Nr_docs) {
    matriz_parse <- rbind(matriz_parse, lista_parse[[i]])
}
df_parse <- as.data.frame(matriz_parse)

# Tag frequencies ---------------------------------------------------------

aux <- df_parse %>%
    group_by(UPOSTAG) %>%
    summarise(n = n())
ggplot(aux, aes(x = reorder(UPOSTAG, -n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("Tag") +
    ggtitle("Tag frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Dependency frequencies ------------------------------------------------


aux <- df_parse %>%
    group_by(DEPREL) %>%
    summarise(n = n())
ggplot(aux, aes(x = reorder(DEPREL, -n), n)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("Tags") +
    ggtitle("Dependency frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Noun frequencies -------------------------------------------------------


print("NOUNS")
aux <- df_parse %>% filter(UPOSTAG %in% c("NOUN", "PROPN"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "nouns")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "nouns")
}

ggplot(aux[1:20, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("nouns") +
    ggtitle("Noun frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Adjective frequencies --------------------------------------------------


print("ADJECTIVES")
aux <- df_parse %>% filter(UPOSTAG %in% c("ADJ"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "adjectives")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "adjectives")
}

ggplot(aux[1:20, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("adjectives") +
    ggtitle("Adjective frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Verb frequencies --------------------------------------------------------


print("VERBS")
aux <- df_parse %>% filter(UPOSTAG %in% c("VERB", "AUX"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "verbs")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "verbs")
}

ggplot(aux[1:20, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("verbs") +
    ggtitle("Verb frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Adverb frequencies ------------------------------------------------------


print("ADVERBS")
aux <- df_parse %>% filter(UPOSTAG %in% c("ADV"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "adverbs")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "adverbs")
}

ggplot(aux[1:20, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("adverbs") +
    ggtitle("Adverb frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Conjunction frequencies -------------------------------------------------


print("CONJUNCTIONS")
aux <- df_parse %>% filter(UPOSTAG %in% c("SCONJ", "CCONJ"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "conjunctions")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "conjunctions")
}

ggplot(aux[1:20, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("conjunctions") +
    ggtitle("Conjunction frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Pronoun frequencies -----------------------------------------------------


print("PRONOUNS")
aux <- df_parse %>% filter(UPOSTAG %in% c("PRON"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "pronouns")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "pronouns")
}

ggplot(aux[1:20, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("pronouns") +
    ggtitle("Pronoun frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Interjection rfequencies ------------------------------------------------


print("INTERJECTIONS")
aux <- df_parse %>% filter(UPOSTAG %in% c("INTJ"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "interjections")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "interjections")
}

# ggplot(aux[1:10,],aes(x = reorder(FORM,-tot), tot)) +
#  geom_bar(stat="identity") +
#  ylab("Frequency") + xlab("interjections") + ggtitle("Interjection frequencies") +
#  theme_bw() + theme(axis.text.x=element_text(angle=45, hjust=1))

# Determiner frequencies --------------------------------------------------


print("DETERMINERS")
aux <- df_parse %>% filter(UPOSTAG %in% c("DET"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "determiner")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "determiner")
}

ggplot(aux[1:10, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("determiner") +
    ggtitle("Determiner frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Punctuation frequencies -------------------------------------------------

print("PUNCTUATION")
aux <- df_parse %>% filter(UPOSTAG %in% c("PUNCT"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "punctuation")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "punctuation")
}

ggplot(aux[1:10, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("punctuation") +
    ggtitle("Punctuation frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Number frequencies ------------------------------------------------------

print("NUMERALS")
aux <- df_parse %>% filter(UPOSTAG %in% c("NUM"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "numeral")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "numeral")
}

ggplot(aux[1:20, ], aes(x = reorder(FORM, -tot), tot)) +
    geom_bar(stat = "identity") +
    ylab("Frequency") +
    xlab("numerals") +
    ggtitle("Numeral frequencies") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Symbol frequencies ------------------------------------------------------

print("SYMBOLS")
aux <- df_parse %>% filter(UPOSTAG %in% c("SYM"))
aux$FORM <- tolower(aux$FORM)
aux <- aux %>%
    group_by(FORM) %>%
    summarise(tot = n()) %>%
    arrange(desc(tot))

if (length(aux$FORM) < 10) {
    knitr::kable(aux, digits = 2, caption = "symbols")
} else {
    knitr::kable(aux[1:10, ], digits = 2, caption = "symbols")
}

if (nrow(aux) < 10) {
    ggplot(aux, aes(x = reorder(FORM, -tot), tot)) +
        geom_bar(stat = "identity") +
        ylab("Frequency") +
        xlab("symbols") +
        ggtitle("Symbol frequencies") +
        theme_bw() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1))
} else {
    ggplot(aux[1:10, ], aes(x = reorder(FORM, -tot), tot)) +
        geom_bar(stat = "identity") +
        ylab("Frequency") +
        xlab("symbols") +
        ggtitle("Symbol frequencies") +
        theme_bw() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1))
}


# Formality ---------------------------------------------------------------
df$formality <- unlist(formality_)

ggplot(df, aes(x = publish_date, y = formality)) +
    geom_line(size = 1.75) +
    ggtitle("Formality") +
    ylab("formality") +
    xlab("year") +
    geom_smooth(method = "loess", size = 1.75) +
    theme_bw() +
    scale_x_date(labels = date_format("%Y"), date_breaks = "1 year") +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.1, hjust = 1),
          text = element_text(size = 18))
    

# Lexical Distance --------------------------------------------------------
df$lexical_density <- unlist(lexical_density_)

ggplot(df, aes(x = publish_date, y = lexical_density)) +
    geom_line(size = 1.75) +
    ggtitle("Lexical Density") +
    ylab("lexical density") +
    xlab("year") +
    geom_smooth(method = "loess", size = 1.75) +
    theme_bw() +
    scale_x_date(labels = date_format("%Y"), date_breaks = "1 year") +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.1, hjust = 1),
          text = element_text(size = 18))
    
