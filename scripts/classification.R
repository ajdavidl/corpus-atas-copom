library(tm)
library(dplyr)
library(lubridate)
library(caret)

Mystopwords <- c("ainda", "ante", "p", "r", "sobre", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro", "mês", "meses", "ano", "anos", as.character(0:9), as.character(1990:2023), tm::stopwords("pt"))
Mystopwords <- c(Mystopwords, "inflação", "preço", "preços", "taxa", "comitê", "copom", "anterior", "política", "monetária", "economia", "relação", "doze", "membro", "cenário")

# loading corpus ----------------------------------------------------------

listAtas <- list.files(path = "../atas", pattern = ".txt", all.files = TRUE, full.names = TRUE)
print(paste(length(listAtas), "atas"))

listText <- c()
for (ata in listAtas) {
  lines <- readLines(con = ata, encoding = "UTF-8")
  lines <- paste(lines, collapse = " ")
  listText <- c(listText, lines)
}
print(paste(length(listText), "atas"))

df <- read.csv2("../decisions.csv", sep = ",")
df[df$meeting == 45 & df$decision == "keep", "meeting"] <- NA
df <- df %>% na.omit()
df <- df %>% arrange(meeting)

df$text <- listText
colnames(df) <- c("doc_id", "selic", "decision", "text")
df$selic <- NULL

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

dtm <- DocumentTermMatrix(docs)
dtm = removeSparseTerms(dtm, 0.98)

# data --------------------------------------------------------------------

data <- data.frame(as.matrix(dtm))
data$id <- rownames(data)
data$decision <- df$decision

partition = createDataPartition(data$decision, p = 0.7, list = FALSE)

dataTrain = data[partition,]
dataTest  = data[-partition,]
dim(dataTrain)
dim(dataTest)
 
dataTest$id <- NULL
dataTrain$id <- NULL

# Machine learning models -------------------------------------------------

control <- trainControl(method = "repeatedcv", #boot, cv, LOOCV, timeslice OR adaptive etc.
                        number = 5,
                        repeats = 10,
                        classProbs = TRUE,
                        savePredictions = "final",
                        allowParallel = TRUE)

model_decisionTree = caret::train(decision ~ .,
                                    data         = dataTrain,
                                    trControl    = control,
                                    metric       = "Accuracy",
                                    method       = 'rpart')

print(model_decisionTree)
rattle::fancyRpartPlot(model_decisionTree$finalModel)
modelLookup('rpart')

grid.search = expand.grid(cp = seq(0, 1, length.out = 5))
model_decisionTree2 = caret::train(decision ~ .,
                                    data         = dataTrain,
                                    trControl    = control,
                                    metric       = "Accuracy",
                                    method       = 'rpart',
                                    tuneGrid     = grid.search)

print(model_decisionTree2)
rattle::fancyRpartPlot(model_decisionTree2$finalModel)

# SVM ---------------------------------------------------------------------
 
control <- trainControl(method = "repeatedcv", #boot, cv, LOOCV, timeslice OR adaptive etc.
                        number = 10,
                        repeats = 5,
                        classProbs = TRUE,
                        savePredictions = "final",
                        allowParallel = TRUE)

model_svm = caret::train(decision ~ .,
                         data         = dataTrain,
                         trControl    = control,
                         metric       = "ROC",
                         tuneLength   = 10,
                         method       = 'svmRadial')

print(model_svm)

grid.search = expand.grid(C = seq(8, 128, length.out =  4),
                          sigma = seq(0, 0.1, length.out = 4))
 
model_svm2 = caret::train(decision ~ .,
                          data         = dataTrain,
                          trControl    = control,
                          metric       = "Accuracy",
                          method       = 'svmRadial',
                          tuneGrid     = grid.search)

print(model_svm2)
