const fs = require('fs');
const path = require('path');

// Set the directory path
const directoryPath = '../atas';


function charFrequency(text) {
    // Split the text into an array of chars
    const chars = text.split('');

    // Create an object to store the frequency of each char
    const frequency = {};

    // Iterate over the chars array and update the frequency object
    chars.forEach(function (char) {

        // If the char already exists in the frequency object, increment its count
        if (frequency[char]) {
            frequency[char]++;
        }
        // Otherwise, add it to the frequency object with a count of 1
        else {
            frequency[char] = 1;
        }
    });

    // Return the frequency object
    return frequency;
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

    console.log("char frequency:")
    const frequency = charFrequency(corpus);
    //console.log(frequency);
    // Convert the dictionary into an array of key-value pairs
    const freq = Object.entries(frequency);
    // Sort the array by values in descending order
    freq.sort((a, b) => b[1] - a[1]);
    // Create a new dictionary from the sorted array
    //const sortedFrequency = Object.fromEntries(freq);
    console.log(freq.slice(0, 20))


});

