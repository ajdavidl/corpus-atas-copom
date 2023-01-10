# Based on http://quanteda.io/articles/pkgdown/examples/plotting.html
library(quanteda)
library(quanteda.textplots)
library(quanteda.textstats)
library(dplyr)
library(ggplot2)
library(quanteda.textmodels)
theme_set(theme_bw())


# stop words --------------------------------------------------------------


Mystopwords <- c('ainda','ante','p','r','sobre', 'janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro','mês','meses','ano','anos', as.character(0:9), as.character(1990:2023), tm::stopwords('pt'))

# loading corpus ----------------------------------------------------------

listAtas <- list.files(path="../atas", pattern=".txt", all.files=TRUE, full.names=TRUE)

print(paste(length(listAtas),"atas"))

listText <- c()
for(ata in listAtas){
  lines <- readLines(con = ata, encoding = "UTF-8")
  lines <- paste(lines, collapse = " ")
  listText <- c(listText,lines)
}
print(paste(length(listText),"atas"))

df <- read.csv2("../decisions.csv", sep = ",")
df[df$meeting==45 & df$decision=="keep", "meeting"] <- NA
df <- df %>% na.omit()
df <- df %>% arrange(meeting)


corp <- corpus(listText, docnames = substr(listAtas, 9,14), docvars = df$decision)
summary(corp)

# wordcloud ---------------------------------------------------------------

corp %>% 
  dfm(remove = Mystopwords, remove_punct = TRUE) %>%
  dfm_trim(min_termfreq = 10, verbose = FALSE) %>% 
  textplot_wordcloud()


corp %>%
  tokens(remove_punct = TRUE) %>%
  tokens_remove(Mystopwords) %>%
  dfm() %>%
  dfm_group(groups = docvars) %>%
  dfm_trim(min_termfreq = 5, verbose = FALSE) %>%
  textplot_wordcloud(comparison = TRUE)

corp %>%
  tokens(remove_punct = TRUE) %>%
  tokens_remove(Mystopwords) %>%
  dfm() %>%
  textplot_wordcloud(min_count = 10,
                   color = c('red', 'pink', 'green', 'purple', 'orange', 'blue'))

# lexical dispersion ------------------------------------------------------

lastAtas <- substr(tail(listAtas,10), 9,14)

corp_subset <- corpus_subset(corp, subset = names(corp) %in% lastAtas)
kwic(tokens(corp_subset), pattern = "inflação") %>%
  textplot_xray()

g <- textplot_xray(
  kwic(corp_subset, pattern = "incerteza"),
  kwic(corp_subset, pattern = "juros"),
  kwic(corp_subset, pattern = "câmbio")
)
g

g <- textplot_xray(
  kwic(corp_subset, pattern = "atividade"),
  kwic(corp_subset, pattern = "preços"),
  kwic(corp_subset, pattern = "taxa"),
  scale = "absolute"
)
g


g <- textplot_xray(
  kwic(corp_subset, pattern = "copom"),
  kwic(corp_subset, pattern = "produção"),
  kwic(corp_subset, pattern = "crescimento")
)
g + aes(color = keyword) + 
  scale_color_manual(values = c("blue", "red", "green")) +
  theme(legend.position = "none")

g

# frequency plot ----------------------------------------------------------

features_corp <- corp %>%
  tokens(remove_punct = TRUE) %>%
  tokens_remove(Mystopwords) %>%
  dfm() %>% textstat_frequency(n = 100)

# Sort by reverse frequency order
features_corp$feature <- with(features_corp, reorder(feature, -frequency))

ggplot(features_corp, aes(x = feature, y = frequency)) +
  geom_point() + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Get frequency grouped by president
freq_grouped <- textstat_frequency(dfm(tokens(corp)), 
                                   groups = docvars)

# Filter the term "american"
freq_inflation <- subset(freq_grouped, freq_grouped$feature %in% "inflação")  

ggplot(freq_inflation, aes(x = group, y = frequency)) +
  geom_point() + 
  xlab(NULL) + 
  ylab("Frequency") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))


dfm_rel_freq <- dfm_weight(dfm(tokens(corp)), scheme = "prop") * 100

rel_freq <- textstat_frequency(dfm_rel_freq, groups = docvars)

# Filter the term "american"
rel_freq_inflation <- subset(rel_freq, feature %in% "inflação")  

ggplot(rel_freq_inflation, aes(x = group, y = frequency)) +
  geom_point() + 
  xlab(NULL) + 
  ylab("Relative frequency") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))





dfm_weight_corp <- corp %>%
  tokens(remove_punct = TRUE) %>%
  tokens_remove(Mystopwords) %>%
  dfm() %>%
  dfm_weight(scheme = "prop")

# Calculate relative frequency by decision
freq_weight <- textstat_frequency(dfm_weight_corp, n = 10, 
                                  groups = docvars)

ggplot(data = freq_weight, aes(x = nrow(freq_weight):1, y = frequency)) +
  geom_point() +
  facet_wrap(~ group, scales = "free") +
  coord_flip() +
  scale_x_continuous(breaks = nrow(freq_weight):1,
                     labels = freq_weight$feature) +
  labs(x = NULL, y = "Relative frequency")


# keyness -----------------------------------------------------------------

# Only select atas by raise and lower
corpus_lower_raise <- corpus_subset(corp, 
                             docvars %in% c("lower", "raise"))

# Create a dfm grouped by president
pres_dfm <- tokens(corpus_lower_raise, remove_punct = TRUE) %>%
  tokens_remove(Mystopwords) %>%
  tokens_group(groups = docvars) %>%
  dfm()

# Calculate keyness and determine Trump as target group
result_keyness <- textstat_keyness(pres_dfm, target = "raise")

# Plot estimated word keyness
textplot_keyness(result_keyness) 

# wordscores --------------------------------------------------------------

# Transform corpus to dfm
corp_dfm <- dfm(corp)

# Set reference scores
refscores <- seq ( from = -round(length(listAtas)/2,0), length.out=length(listAtas))

# Predict Wordscores model
ws <- textmodel_wordscores(corp_dfm, y = refscores, smooth = 1)

# Plot estimated word positions (highlight words and print them in red)
textplot_scale1d(ws,
                 highlighted = c("inflação", "preço", "taxa", "juros", "selic"), 
                 highlighted_color = "red")


# Get predictions
#pred <- predict(ws, se.fit = TRUE)

# Plot estimated document positions and group by "party" variable
#textplot_scale1d(pred, margin = "documents",
#                 groups = docvars(corp))


# wordfish ----------------------------------------------------------------

lastAtas <- substr(tail(listAtas,10), 9,14)

corp_subset <- corpus_subset(corp, subset = names(corp) %in% lastAtas)

wf <- textmodel_wordfish(dfm(tokens(corp_subset)))

# Plot estimated word positions
textplot_scale1d(wf,
                 highlighted = c("inflação", "preço", "taxa", "juros", "selic"), 
                 highlighted_color = "red")

# Correspondence Analysis -------------------------------------------------

# Run correspondence analysis on dfm
#ca <- textmodel_ca(dfm(tokens(corp_subset)))

# Plot estimated positions and group 
#textplot_scale1d(ca, margin = "documents",
#                 groups = docvars(corp_subset))
