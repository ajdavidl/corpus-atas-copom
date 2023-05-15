const fs = require('fs');
const path = require('path');

// Set the directory path
const directoryPath = '../atas';

// Function that calculate the metrics
function calculateMetrics(text) {
    // Count number of words
    const words = text.split(/\s+/);
    const wordCount = words.length;

    // Count number of characters with spaces
    const charCountWithSpaces = text.length;

    // Count number of characters without spaces
    const charCountWithoutSpaces = text.replace(/\s+/g, '').length;

    // Count number of sentences
    const sentences = text.split(/[.?!]+/);
    const sentenceCount = sentences.length - 1;

    // Calculate other metrics
    const charsPerWords = charCountWithoutSpaces / wordCount;
    const wordsPerSentence = wordCount / sentenceCount;

    // Return an object containing the calculated metrics
    return {
        charCountWithSpaces,
        charCountWithoutSpaces,
        wordCount,
        sentenceCount,
        charsPerWords,
        wordsPerSentence,
    };
}


// Read all files in the directory
fs.readdir(directoryPath, function (err, files) {
    if (err) {
        console.log('Error reading directory:', err);
        return;
    }

    // Filter the files to only include text files
    const textFiles = files.filter(function (file) {
        return path.extname(file).toLowerCase() === '.txt';
    });

    // Read the contents of each text file and store them in an array
    const contents = [];
    textFiles.forEach(function (file) {
        const filePath = path.join(directoryPath, file);
        const fileContents = fs.readFileSync(filePath, 'utf8');
        contents.push(fileContents);
    });

    console.log(contents.length, "atas");
    const corpus = contents.join(' ');
    const metrics = calculateMetrics(corpus);
    console.log(metrics);

});