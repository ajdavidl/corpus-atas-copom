#!/bin/bash

# Function to count the number of characters in a file
count_characters() {
    characters=$(wc -m < "$1")
    echo "$characters"
}

# Function to count the number of words in a file
count_words() {
    words=$(wc -w < "$1")
    echo "$words"
}

# Function to count the number of sentences in a file
count_sentences() {
    sentences=$(grep -c '\.' "$1")
    echo "$sentences"
}

# Directory path
directory="../atas"

# Variables to store the total counts
total_characters=0
total_words=0
total_sentences=0

# Iterate over text files in the directory
for file in "$directory"/*.txt; do
    if [ -f "$file" ]; then
        characters=$(count_characters "$file")
        words=$(count_words "$file")
        sentences=$(count_sentences "$file")

        total_characters=$((total_characters + characters))
        total_words=$((total_words + words))
        total_sentences=$((total_sentences + sentences))
    fi
done

# Print the total counts
echo $(ls ../atas/ | wc -l) Documents
echo "Number of characters: $total_characters"
echo "Number of words: $total_words"
echo "Number of sentences: $total_sentences"
echo "Number of words per sentence: $((total_words / total_sentences))"
