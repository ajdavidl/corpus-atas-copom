
listAtas <- list.files(path="../atas", pattern=".txt", all.files=TRUE, full.names=TRUE)

corpus <- c()
for(ata in listAtas){
    lines <- readLines(con = ata, encoding = "UTF-8")
    lines <- paste(lines, collapse = " ")
    corpus <- c(corpus,lines)
}
print(paste(length(corpus),"atas"))

corpusJoined <- paste(corpus, collapse = ' ')
corpusJoinedWithoutPunctuation <- tm::removePunctuation(corpusJoined)
corpusWordTokenized <- tokenizers::tokenize_words(corpusJoined, simplify = TRUE)
corpusWordTokenizedWithoutPunctuation <- tokenizers::tokenize_words(corpusJoinedWithoutPunctuation, simplify = TRUE)
corpusJoinedWithoutSpaces <- gsub(pattern = " ", replacement = "", x = corpusJoined)
corpusSentences <- tokenizers::tokenize_sentences(corpusJoined,simplify = TRUE)

print(paste0("Number of characters with spaces: ", nchar(corpusJoined)))
print(paste0("Number of characters without spaces: ", nchar(corpusJoinedWithoutSpaces)))
print(paste0("Number of words: ",length(corpusWordTokenizedWithoutPunctuation)))
print(paste0("Number of sentences: ", length(corpusSentences)))
print(paste0("Number of characters per words: ", nchar(corpusJoinedWithoutSpaces)/length(corpusWordTokenizedWithoutPunctuation)))
print(paste0("Number of words per sentence: ", length(corpusWordTokenizedWithoutPunctuation)/length(corpusSentences)))
