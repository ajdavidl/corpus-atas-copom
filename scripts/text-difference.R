source("load_texts.R", encoding = "UTF-8")

df <-return_data_frame()

last = df$text[length(df$text)]
penultimate = df$text[length(df$text)-1]
lst <- strsplit(c(last = last, penultimate = penultimate), "(?<=[.])\\s", perl = TRUE)
un1 <- unique(unlist(lst))
result <- lapply(lst, setdiff, x = un1)

print(result$last)
