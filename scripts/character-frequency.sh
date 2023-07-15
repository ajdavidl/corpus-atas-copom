#!/bin/bash

# Directory path
directory="../atas"

# Array to store character frequencies
declare -a char_frequency

# Iterate over text files in the directory
for file in "$directory"/*.txt; do
    echo $file
    if [ -f "$file" ]; then
        # Read each character from the file
        while IFS= read -r -n1 char; do
            # Ignore whitespace characters
            if [[ ! $char =~ ^[[:space:]]$ ]]; then
                # Get the ASCII value of the character
                ascii_val=$(printf '%d' "'$char")
                # Increment the frequency of the character
                ((char_frequency[ascii_val]++))
            fi
        done < "$file"
    fi
done

# Print the character frequencies
echo "Character frequencies:"
for ascii_val in "${!char_frequency[@]}"; do
    char=$(printf \\$(printf '%03o' "$ascii_val"))
    frequency=${char_frequency[$ascii_val]}
    echo "$char: $frequency"
done
