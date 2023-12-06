#!/bin/bash

# Directory path
directory="../atas"

# Temporary file to store all words
temp_file=$(mktemp)

# Associative array to store word frequencies
declare -A word_frequency

# Iterate over text files in the directory
for file in "$directory"/*.txt; do
    if [ -f "$file" ]; then
        # Extract words from the file, convert to lowercase, and append to the temporary file
        tr -s '[:space:]' '\n' < "$file" | grep -oE '\w+' | tr '[:upper:]' '[:lower:]' >> "$temp_file"
    fi
done

# Count the frequency of each word
while IFS= read -r word; do
    ((word_frequency["$word"]++))
done < "$temp_file"

# Remove the temporary file
rm "$temp_file"

# Create new temporary file
temp_file=$(mktemp)

for word in $(printf "%s\n" "${!word_frequency[@]}"); do
    frequency=${word_frequency["$word"]}
    printf "%-10s %d\n" "$word" "$frequency" >> "$temp_file"
done

# Print the table with the most frequent words
echo "Word      Frequency"
echo "-------------------"
sort -nr -k2 "$temp_file" | head -n 25

# Remove the temporary file
rm "$temp_file"
