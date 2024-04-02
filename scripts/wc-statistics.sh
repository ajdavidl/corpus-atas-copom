#!/bin/bash

# This script was made by GPT-4.

# Directory containing the text files.
TEXT_DIR="../atas"

# Counters initialization
total_lines=0
total_words=0
total_chars=0
file_count=0

# Loop through all text files in the directory
for file in "$TEXT_DIR"/*.txt
do
  # Counters for individual files
  lines=$(wc -l < "$file")
  words=$(wc -w < "$file")
  chars=$(wc -m < "$file")

  echo "Statistics for $file:"
  echo "Lines: $lines"
  echo "Words: $words"
  echo "Characters: $chars"
  echo

  # Update total counters
  total_lines=$((total_lines + lines))
  total_words=$((total_words + words))
  total_chars=$((total_chars + chars))
  file_count=$((file_count + 1))
done

# Display total statistics
echo "Total statistics for $file_count files:"
echo "Total Lines: $total_lines"
echo "Total Words: $total_words"
echo "Total Characters: $total_chars"