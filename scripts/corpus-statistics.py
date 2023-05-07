import re
import nltk
import os

listAtas = os.listdir("../atas")

corpus = []

for ata in listAtas:
    with open("../atas/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines)
            corpus.append(lines)

print(len(corpus), "atas")

corpusJoined = ' '.join(corpus)
corpusJoinedWithoutPunctuation = re.sub(r'[^\w\s]', '', corpusJoined)
corupsWordTokenized = nltk.word_tokenize(corpusJoined)
corupsWordTokenizedWithoutPunctuation = nltk.word_tokenize(
    corpusJoinedWithoutPunctuation)
corpusJoinedWithoutSpaces = re.sub(' ', '', corpusJoined)
corpusSentences = nltk.tokenize.sent_tokenize(corpusJoined)

print("Number of characters with spaces: ", len(corpusJoined))
print("Number of characters without spaces: ", len(corpusJoinedWithoutSpaces))
print("Number of words: ", len(corupsWordTokenizedWithoutPunctuation))
print("Number of sentences: ", len(corpusSentences))
print("Number of characters per words: ", len(
    corpusJoinedWithoutSpaces)/len(corupsWordTokenizedWithoutPunctuation))
print("Number of words per sentence: ", len(
    corupsWordTokenizedWithoutPunctuation)/len(corpusSentences))
