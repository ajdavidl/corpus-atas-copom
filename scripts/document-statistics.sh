#!/bin/bash

# This script was made by GPT-4.

# Example of use:
# $ ./document-statistics.sh ../atas/ata260.txt

# Checking if a file was provided as an argument
if [ $# -eq 0 ]; then
    echo "You need to provide a text file as an argument."
    exit 1
fi

# Assigning the file to a variable
FILE=$1

# Counting lines, words and characters
echo "Lines: $(wc -l < "$FILE")"
echo "Words: $(wc -w < "$FILE")"
echo "Characters: $(wc -c < "$FILE")"

# Counting the frequency of each word
echo "Word frequency:"
tr '[:space:]' '[\n*]' < "$FILE" | grep -v "^\s*$" | sort | uniq -c | sort -bnr