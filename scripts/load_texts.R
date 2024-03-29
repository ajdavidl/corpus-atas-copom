library(dplyr)

read_text_files <- function(){
  listAtas <- list.files(path = "../atas", pattern = ".txt", all.files = TRUE, full.names = TRUE)
  listText <- c()
  for (ata in listAtas) {
    lines <- readLines(con = ata, encoding = "UTF-8")
    lines <- paste(lines, collapse = " ")
    listText <- c(listText, lines)
  }
  return(listText)
}

return_data_frama <- function(){
  listText <- read_text_files()
  df <- read.csv2("../decisions.csv", sep = ",")
  df[df$meeting == 45 & df$decision == "keep", "meeting"] <- NA
  df <- df %>% na.omit()
  df <- df %>% arrange(meeting)
  
  df$text <- listText
  colnames(df) <- c("meeting", "selic", "decision", "text")
  
  df2 <- read.csv2("../copom_dates.csv", sep = ",", stringsAsFactors = FALSE)
  colnames(df2) <- c("meeting", "begin_date", "end_date", "publish_date")
  
  df <- df %>% left_join(df2, by = "meeting")
  rm(df2)
  return(df)
}