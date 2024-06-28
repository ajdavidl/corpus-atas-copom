println("Julia version: ", VERSION)

using DataFrames
using Plots
using FreqTables
using TextAnalysis
using Languages
using WordCloud

Mystopwords = stopwords(Languages.Portuguese);

println("Number of stopwords: ", length(Mystopwords))

#Create a corpus

listAtas = readdir("../atas");
corpus = []

for i in eachindex(listAtas)
    f = open("../atas/" * listAtas[i])
    txt = readlines(f)
    push!(corpus, txt)
end

println(length(corpus), " atas")


docs = []
for i in eachindex(listAtas)
    fd = FileDocument("../atas/" * listAtas[i])
    language!(fd, Languages.Portuguese())
    push!(docs, fd)
end
crps = Corpus(docs)
standardize!(crps, StringDocument)
remove_case!(crps)
prepare!(crps, strip_numbers)
prepare!(crps, strip_punctuation)
update_lexicon!(crps)
update_inverse_index!(crps)

#word frequency
#with stop words

dict_words = lexicon(crps);
words = [];
frequency = [];
for (key, value) in dict_words
    push!(words, key)
    push!(frequency, value)
end
words_df = DataFrame(Dict("Words" => words, "n" => frequency));
sort!(words_df, [:n, :Words], rev=[true, false])
println(words_df[1:20, :])
#display(bar(words_df[1:10, 1], words_df[1:10, 2], title="word frequency with stopwords", orientation=:horizontal))

#word frequency
#without stop words

crps2 = deepcopy(crps);
prepare!(crps2, strip_stopwords)
prepare!(crps2, strip_numbers)
prepare!(crps2, strip_punctuation)
remove_case!(crps2)
remove_words!(crps2, Mystopwords)
update_lexicon!(crps2)
update_inverse_index!(crps2)

dict_words2 = lexicon(crps2);
words2 = [];
frequency2 = [];
for (key, value) in dict_words2
    push!(words2, key)
    push!(frequency2, value)
end
words_df2 = DataFrame(Dict("Words" => words2, "n" => frequency2));
sort!(words_df2, [:n, :Words], rev=[true, false])
println(words_df2[1:20, :])
#display(bar(words_df2[1:10, 1], words_df2[1:10, 2], title="word frequency without stopwords", orientation=:horizontal))

#bigram frequency
#with stop words

dict_bigram = Dict{Any,Any}()
for sent in corpus
    doc = StringDocument(lowercase(string(sent)))
    language!(doc, Languages.Portuguese())
    remove_case!(doc)
    prepare!(doc, strip_numbers)
    prepare!(doc, strip_punctuation)
    dict = ngrams(doc, 2) #this function includes 1-gram and 2-grams
    for k in dict
        if ' ' in k[1] # exclude 1-gram
            if haskey(dict_bigram, k[1])
                dict_bigram[k[1]] += k[2]
            else
                dict_bigram[k[1]] = k[2]
            end
        end
    end
end

bigrams = [];
frequency = [];
for (key, value) in dict_bigram
    push!(bigrams, key)
    push!(frequency, value)
end
bigram_df = DataFrame(Dict("Bigram" => bigrams, "n" => frequency));
sort!(bigram_df, [:n, :Bigram], rev=[true, false])
println(bigram_df[1:20, :])
#display(bar(bigram_df[1:10, 1], bigram_df[1:10, 2], title="bigram frequency with stopwords"))

#bigram frequency
#with stop words

dict_bigram2 = Dict{Any,Any}()
for sent in corpus
    doc = StringDocument(lowercase(string(sent)))
    language!(doc, Languages.Portuguese())
    remove_case!(doc)
    prepare!(doc, strip_numbers)
    prepare!(doc, strip_punctuation)
    prepare!(doc, strip_stopwords)
    remove_words!(doc, Mystopwords)
    dict = ngrams(doc, 2) #this function includes 1-gram and 2-grams
    for k in dict
        if ' ' in k[1] # exclude 1-gram
            if haskey(dict_bigram2, k[1])
                dict_bigram2[k[1]] += k[2]
            else
                dict_bigram2[k[1]] = k[2]
            end
        end
    end
end

bigrams2 = [];
frequency2 = [];
for (key, value) in dict_bigram
    push!(bigrams2, key)
    push!(frequency2, value)
end
bigram_df2 = DataFrame(Dict("Bigram" => bigrams2, "n" => frequency2));
sort!(bigram_df2, [:n, :Bigram], rev=[true, false])
println(bigram_df2[1:20, :])
#display(bar(bigram_df[1:10, 1], bigram_df[1:10, 2], title="bigram frequency without stopwords"))

#trigram frequency
#with stop words

dict_trigram = Dict{Any,Any}()
for sent in corpus
    doc = StringDocument(lowercase(string(sent)))
    language!(doc, Languages.Portuguese())
    remove_case!(doc)
    prepare!(doc, strip_numbers)
    prepare!(doc, strip_punctuation)
    dict = ngrams(doc, 3) #this function includes 1-gram, 2-grams and 3-grams
    for k in dict
        if count(c -> (c == ' '), k[1]) == 2 # exclude 1-gram and 2-gram
            if haskey(dict_trigram, k[1])
                dict_trigram[k[1]] += k[2]
            else
                dict_trigram[k[1]] = k[2]
            end
        end
    end
end

trigrams = [];
frequency = [];
for (key, value) in dict_trigram
    push!(trigrams, key)
    push!(frequency, value)
end
trigram_df = DataFrame(Dict("Trigram" => trigrams, "n" => frequency));
sort!(trigram_df, [:n, :Trigram], rev=[true, false])
println(trigram_df[1:20, :])
#display(bar(trigram_df[1:10, 1], trigram_df[1:10, 2], title="trigram frequency with stopwords"))

#trigram frequency
#without stop words

dict_trigram2 = Dict{Any,Any}()
for sent in corpus
    doc = StringDocument(lowercase(string(sent)))
    language!(doc, Languages.Portuguese())
    remove_case!(doc)
    prepare!(doc, strip_numbers)
    prepare!(doc, strip_punctuation)
    prepare!(doc, strip_stopwords)
    remove_words!(doc, Mystopwords)
    dict = ngrams(doc, 3) #this function includes 1-gram, 2-grams and 3-grams
    for k in dict
        if count(c -> (c == ' '), k[1]) == 2 # exclude 1-gram and 2-gram
            if haskey(dict_trigram2, k[1])
                dict_trigram2[k[1]] += k[2]
            else
                dict_trigram2[k[1]] = k[2]
            end
        end
    end
end

trigrams2 = [];
frequency2 = [];
for (key, value) in dict_trigram
    push!(trigrams2, key)
    push!(frequency2, value)
end
trigram_df2 = DataFrame(Dict("Trigram" => trigrams2, "n" => frequency2));
sort!(trigram_df2, [:n, :Trigram], rev=[true, false])
println(trigram_df2[1:20, :])
#display(bar(trigram_df[1:10, 1], trigram_df[1:10, 2], title="trigram frequency without stopwords"))