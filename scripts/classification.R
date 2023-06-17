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
pred_decicionTree <- predict(model_decisionTree, newdata = dataTest)
confusionMatrix(pred_decicionTree, as.factor(dataTest$decision))

grid.search = expand.grid(cp = seq(0, 1, length.out = 5))
model_decisionTree2 = caret::train(decision ~ .,
                                    data         = dataTrain,
                                    trControl    = control,
                                    metric       = "Accuracy",
                                    method       = 'rpart',
                                    tuneGrid     = grid.search)

print(model_decisionTree2)
rattle::fancyRpartPlot(model_decisionTree2$finalModel)
pred_decicionTree2 <- predict(model_decisionTree2, newdata = dataTest)
confusionMatrix(pred_decicionTree2, as.factor(dataTest$decision))

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
pred_svm <- predict(model_svm, newdata = dataTest)
confusionMatrix(pred_svm, as.factor(dataTest$decision))

grid.search = expand.grid(C = seq(8, 128, length.out =  4),
                          sigma = seq(0, 0.1, length.out = 4))
 
model_svm2 = caret::train(decision ~ .,
                          data         = dataTrain,
                          trControl    = control,
                          metric       = "Accuracy",
                          method       = 'svmRadial',
                          tuneGrid     = grid.search)

print(model_svm2)
pred_svm2 <- predict(model_svm2, newdata = dataTest)
confusionMatrix(pred_svm2, as.factor(dataTest$decision))

# Define the control parameters for the algorithms
ctrl <- trainControl(method = "cv", number = 10)

# Logistic Regression
# fit_glm <- train(decision ~ ., data = dataTrain, method = "glm", trControl = ctrl)
# pred_glm <- predict(fit_glm, newdata = dataTest)
# confusionMatrix(pred_glm, as.factor(dataTest$decision))

# K-Nearest Neighbors
fit_knn <- train(decision ~ ., data = dataTrain, method = "knn", trControl = ctrl)
pred_knn <- predict(fit_knn, newdata = dataTest)
confusionMatrix(pred_knn, as.factor(dataTest$decision))

# Naive Bayes
fit_nb <- train(decision ~ ., data = dataTrain, method = "naive_bayes", trControl = ctrl)
pred_nb <- predict(fit_nb, newdata = dataTest)
confusionMatrix(pred_nb, as.factor(dataTest$decision))

# Support Vector Machine (SVM)
fit_svm <- train(decision ~ ., data = dataTrain, method = "svmRadial", trControl = ctrl)
pred_svm <- predict(fit_svm, newdata = dataTest)
confusionMatrix(pred_svm, as.factor(dataTest$decision))

