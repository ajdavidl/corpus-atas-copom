using WordTokenizers
using TextAnalysis
using WordCloud
using Plots
using Languages

# Function to read all text files in a directory
function read_text_files(dir::String)::Vector{String}
    texts = String[]
    for file in readdir(dir)
        if endswith(file, ".txt")
            filepath = joinpath(dir, file)
            text = read(filepath, String)
            push!(texts, text)
        end
    end
    return texts
end

# Function to preprocess text (tokenize and remove stop words)
function preprocess_texts(texts::Vector{String})
    stopwords = vcat(Languages.stopwords(Languages.Portuguese), Array(["p", "r"]))
    processed_texts = String[]
    for text in texts
        tokens = WordTokenizers.tokenize(text)
        filtered_tokens = [token for token in tokens if !(lowercase(token) in stopwords)]
        append!(processed_texts, filtered_tokens)
    end
    processed_texts = join(processed_texts, " ", " ")
    return processed_texts
end

# Main script
dir = "../atas"  # Replace with the path to your text files
println("Reading files...")
texts = read_text_files(dir)

# Preprocess the texts and create the word cloud
println("processing texts...")
processed_words = preprocess_texts(texts)

# ploting wordcloud
println("making the wordcloud...")
wc = wordcloud(processed_words) |> generate!
paint(wc, "wordcloud.svg")
run(`firefox wordcloud.svg`)