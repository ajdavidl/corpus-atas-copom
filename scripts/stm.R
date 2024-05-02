library(tm)
library(dplyr)
library(lubridate)
library(tokenizers)
library(stm) # Structural Topic Model

source("load_texts.R", encoding = "UTF-8")

# loading corpus ----------------------------------------------------------
print("Loading files ...")
df_orig <-return_data_frame()
print(paste(as.character(dim(df_orig)[1]), "atas"))

# stop words --------------------------------------------------------------
Mystopwords <- c(Mystopwords, "inflação", "preço", "preços", "taxa", "comitê", 
                 "copom", "anterior", "política", "monetária", "economia", 
                 "relação", "doze", "membro", "cenário","trimestre","trimestres",
                 "afinal","nível","ser","membros","reunião","partir","paulo",
                 "primeiro","segundo")

# Configuration
NrTopics = 20
MaxIterations = 100
STEM = FALSE

PARAGRAPHS <- TRUE

if(PARAGRAPHS){
  meeting <- df_orig$meeting[1]
  selic <- df_orig$selic[1]
  decision <- df_orig$decision[1]
  text <- df_orig$text[1]
  text <- tokenize_paragraphs(text, simplify = TRUE)
  begin_date <- df_orig$begin_date[1]
  end_date <- df_orig$end_date[1]
  publish_date <- df_orig$publish_date[1]
  df_par <- data.frame(meeting = meeting, selic = selic, decision = decision,
                       text = text, begin_date = begin_date, end_date = end_date,
                       publish_date = publish_date)
  for (i in 2:dim(df_orig)[1]) {
    meeting <- df_orig$meeting[i]
    selic <- df_orig$selic[i]
    decision <- df_orig$decision[i]
    text <- df_orig$text[i]
    text <- tokenize_paragraphs(text, simplify = TRUE)
    begin_date <- df_orig$begin_date[i]
    end_date <- df_orig$end_date[i]
    publish_date <- df_orig$publish_date[i]
    df_aux <- data.frame(meeting = meeting, selic = selic, decision = decision,
                         text = text, begin_date = begin_date, end_date = end_date,
                         publish_date = publish_date)
    df_par <- rbind.data.frame(df_par, df_aux)
  }
  df <- df_par
  print(paste(as.character(dim(df)[1]), "paragraphs"))
}else{
  df <- df_orig
}
df$doc_id <- 1:dim(df)[1]
df$date <- df$publish_date

# pre-processing ----------------------------------------------------------

docs <- Corpus(DataframeSource(df))
toSpace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "\n")
docs <- tm_map(docs, toSpace, "\r")
docs <- tm_map(docs, toSpace, "\t")
docs <- tm_map(docs, toSpace, "_")
docs <- tm_map(docs, toSpace, "-")
docs <- tm_map(docs, toSpace, "\\(")
docs <- tm_map(docs, toSpace, "\\)")
docs <- tm_map(docs, toSpace, "'")
docs <- tm_map(docs, toSpace, '"')
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, removePunctuation)
docs <- tm_map(docs, removeWords, Mystopwords)
docs <- tm_map(docs, stripWhitespace)

df$text_clean <- docs$content

# Ingest ------------------------------------------------------------------


processed <- textProcessor(df$text_clean, metadata = df[, c("doc_id", "selic", "decision", "date")],stem = STEM,)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta

# Prepare -----------------------------------------------------------------

plotRemoved(processed$documents, lower.thresh = seq(1, 200, by = 100))
out <- prepDocuments(processed$documents, processed$vocab, processed$meta, lower.thresh = 15)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta

# Estimate ----------------------------------------------------------------

model <- stm(documents = out$documents, vocab = out$vocab, K = NrTopics, prevalence = ~ doc_id + selic + decision + year(date), max.em.its = MaxIterations, data = out$meta, init.type = "Spectral")


# Understand --------------------------------------------------------------


print(labelTopics(model))

for (i in 1:NrTopics) {
  thoughts <- findThoughts(model, texts = df$text[meta$doc_id], n = 1, topics = i)$docs[[1]]
  plotQuote(thoughts, width = 30, main = paste("Topic ",as.character(i)))
}

prep <- estimateEffect(~ doc_id + selic + decision + year(date), model, meta = out$meta, uncertainty = "Global")
print(summary(prep))

for (i in 1:NrTopics) {
  print(summary(prep, topics = i))
}


# Visualize ---------------------------------------------------------------

plot(model, type = "summary", xlim = c(0, 0.3))
