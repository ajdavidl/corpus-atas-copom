println("Julia version: ", VERSION)

using DataFrames
using Plots
using FreqTables
using WordCloud

# Read files

listAtas = readdir("../atas");
corpus = [];

for i in 1:length(listAtas)
    f = open("../atas/" * listAtas[i])
    txt = readlines(f)
    push!(corpus, txt)
end
println(length(corpus), " atas")

# Auxiliary functions
function removeSpecialLetters(text)
    # The SubString function breaks when dealing with the characters below
    text = replace(text, "ç" => "c")
    text = replace(text, "á" => "a")
    text = replace(text, "á" => "a")
    text = replace(text, "à" => "a")
    text = replace(text, "ã" => "a")
    text = replace(text, "â" => "a")
    text = replace(text, "ä" => "a")
    text = replace(text, "é" => "e")
    text = replace(text, "ê" => "e")
    text = replace(text, "í" => "i")
    text = replace(text, "ó" => "o")
    text = replace(text, "õ" => "o")
    text = replace(text, "ô" => "o")
    text = replace(text, "ú" => "u")
    text = replace(text, "ü" => "u")
    text = replace(text, "º" => " ")
    text = replace(text, "Á" => "A")
    text = replace(text, "À" => "A")
    text = replace(text, "Ã" => "A")
    text = replace(text, "Â" => "A")
    text = replace(text, "É" => "E")
    text = replace(text, "Ê" => "E")
    text = replace(text, "Í" => "I")
    text = replace(text, "Ó" => "O")
    text = replace(text, "Õ" => "O")
    text = replace(text, "Ô" => "O")
    text = replace(text, "Ú" => "U")
    text = replace(text, "Ü" => "U")
    text = replace(text, "Ç" => "C")
    text = replace(text, "ñ" => "n")
    text = replace(text, "Ñ" => "N")
    text = replace(text, "°" => " ")
    text = replace(text, "“" => " ")
    text = replace(text, "”" => " ")
    text = replace(text, "ª" => " ")
    text = replace(text, "’" => " ")
    text = replace(text, "´" => " ")
    text = replace(text, "–" => " ")
    text = replace(text, "‑" => " ")
    text = replace(text, "—" => " ")
    text = replace(text, "─" => " ")
    text = replace(text, "±" => " ")
    text = replace(text, "+" => " ")
    text = replace(text, "¥" => " ")
    text = replace(text, "£" => " ")
    text = replace(text, "€" => " ")
    text = replace(text, "\uad" => " ")
    return text
end
ngram(s::AbstractString, n) = [SubString(s, i:i+n-1) for i = 1:length(s)-n+1]

global NRTOKENS = 30
println("Counting chars...")
dict_char = Dict{Char,Int}()
for txt in corpus
    for char in string(txt)
        if haskey(dict_char, char)
            dict_char[char] += 1
        else
            dict_char[char] = 1
        end
    end
end

chars = [];
frequency = [];
for (key, value) in dict_char
    push!(chars, key)
    push!(frequency, value)
end
char_df = DataFrame(Dict("Char" => chars, "n" => frequency));
sort!(char_df, [:n, :Char], rev=[true, false]);
println(char_df[1:NRTOKENS, :])

println("Counting 2-chars...")
dict_2gram = Dict{String,Int}()
for txt in corpus
    s = ""
    for t in txt
        s = s * " " * t
    end
    []
    s = removeSpecialLetters(s)
    for ngr in ngram(s, 2)
        if haskey(dict_2gram, ngr)
            dict_2gram[ngr] += 1
        else
            dict_2gram[ngr] = 1
        end
    end
end

chars = [];
frequency = [];
for (key, value) in dict_2gram
    push!(chars, key)
    push!(frequency, value)
end
bigram_df = DataFrame(Dict("Char" => chars, "n" => frequency));
sort!(bigram_df, [:n, :Char], rev=[true, false]);
println(bigram_df[1:NRTOKENS, :])

println("Counting 3-chars...")
dict_3gram = Dict{String,Int}()
for txt in corpus
    s = ""
    for t in txt
        s = s * " " * t
    end
    []
    s = removeSpecialLetters(s)
    for ngr in ngram(s, 3)
        if haskey(dict_3gram, ngr)
            dict_3gram[ngr] += 1
        else
            dict_3gram[ngr] = 1
        end
    end
end

chars = [];
frequency = [];
for (key, value) in dict_3gram
    push!(chars, key)
    push!(frequency, value)
end
trigram_df = DataFrame(Dict("Char" => chars, "n" => frequency));
sort!(trigram_df, [:n, :Char], rev=[true, false]);
println(trigram_df[1:NRTOKENS, :])

println("Counting 4-chars...")
dict_4gram = Dict{String,Int}()
for txt in corpus
    s = ""
    for t in txt
        s = s * " " * t
    end
    []
    s = removeSpecialLetters(s)
    for ngr in ngram(s, 4)
        if haskey(dict_4gram, ngr)
            dict_4gram[ngr] += 1
        else
            dict_4gram[ngr] = 1
        end
    end
end

chars = [];
frequency = [];
for (key, value) in dict_4gram
    push!(chars, key)
    push!(frequency, value)
end
fourgram_df = DataFrame(Dict("Char" => chars, "n" => frequency));
sort!(fourgram_df, [:n, :Char], rev=[true, false]);
println(fourgram_df[1:NRTOKENS, :])


