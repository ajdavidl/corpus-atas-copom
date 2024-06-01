const fs = require('fs');
const path = require('path');

// Function to read a file and return its contents as a string
function readFile(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    });
}

// Function to compare two strings and return the differences
function compareFiles(content1, content2) {
    const lines1 = content1.split('\n');
    const lines2 = content2.split('\n');

    const maxLength = Math.max(lines1.length, lines2.length);
    const differences = [];

    for (let i = 0; i < maxLength; i++) {
        const line1 = lines1[i] || '';
        const line2 = lines2[i] || '';

        if (line1 !== line2) {
            differences.push(`Line ${i + 1}:\n  File1: ${line1}\n  File2: ${line2}`);
        }
    }

    return differences;
}

// Function to show differences between two files
async function showFileDifferences(filePath1, filePath2) {
    try {
        const content1 = await readFile(filePath1);
        const content2 = await readFile(filePath2);

        const differences = compareFiles(content1, content2);

        if (differences.length > 0) {
            console.log('Differences found:');
            differences.forEach(diff => console.log(diff));
        } else {
            console.log('The files are identical.');
        }
    } catch (err) {
        console.error('Error reading files:', err);
    }
}

const directoryPath = '../atas';
// Example usage
const files = fs.readdirSync(directoryPath);
const filePath1 = path.join(__dirname, directoryPath, files.slice(-2)[0]);
const filePath2 = path.join(__dirname, directoryPath, files.slice(-1)[0]);

console.log("File 1: " + filePath1)
console.log("File 2: " + filePath2)

showFileDifferences(filePath1, filePath2);
