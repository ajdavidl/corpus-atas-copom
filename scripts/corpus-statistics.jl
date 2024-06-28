using WordTokenizers

listAtas = readdir("../atas");
corpus = [];

for i in eachindex(listAtas)
    f = open("../atas/" * listAtas[i])
    txt = readlines(f)
    push!(corpus, txt)
end
println(length(corpus), " atas")

corpus = join(corpus, " ");

function text_stats(text::AbstractString)
    num_words = length(split(text))
    num_chars_with_spaces = length(text)
    num_chars_without_spaces = length(replace(text, " " => ""))
    num_sentences = length(split_sentences(text))
    num_chars_per_word = num_chars_without_spaces / num_words
    num_words_per_sentence = num_words / num_sentences

    return num_words, num_chars_with_spaces, num_chars_without_spaces, num_sentences, num_chars_per_word, num_words_per_sentence
end

num_words, num_chars_with_spaces, num_chars_without_spaces, num_sentences, num_chars_per_word, num_words_per_sentence = text_stats(corpus)
println("Number of characters (with spaces): ", num_chars_with_spaces)
println("Number of characters (without spaces): ", num_chars_without_spaces)
println("Number of words: ", num_words)
println("Number of sentences: ", num_sentences)
println("Number of characters per words: ", num_chars_per_word)
println("Number of words per sentence: ", num_words_per_sentence)