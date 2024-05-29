#!/bin/bash

echo "Differences between last 2 minutes."

# Directory containing the text files.
TEXT_DIR="../atas"

file1="$(ls $TEXT_DIR | tail -n 2 | head -n 1)"
file2="$(ls $TEXT_DIR | tail -n 1)"

echo "Comparing $file1 and $file2"

text1="$(cat $TEXT_DIR/$file1)"
text2="$(cat $TEXT_DIR/$file2)"

diff --color=always <(echo "$text1") <(echo "$text2")