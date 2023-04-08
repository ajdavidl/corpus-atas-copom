import re
import nltk
import os
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import numpy as np
import wordcloud

listAtas = os.listdir("../atas")

corpus = []

for ata in listAtas:
    with open("../atas/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines)
            corpus.append(lines)

print(len(corpus), "atas")

numberOfChars = 25
for i in range(1, 5):
    print(i, "characters")
    charCountVect = CountVectorizer(
        analyzer='char', ngram_range=(i, i), lowercase=False)
    charCountVect.fit(corpus)

    bagOfChar = charCountVect.transform(corpus)
    sumChars = bagOfChar.sum(axis=0)
    charsFreq = [(char, sumChars[0, idx])
                 for char, idx in charCountVect.vocabulary_.items()]
    charsFreq = sorted(charsFreq, key=lambda x: x[1], reverse=True)
    print(charsFreq[:50])
    yPos = np.arange(numberOfChars)
    objects = []
    performance = []
    for i in range(numberOfChars):
        aux = charsFreq[i]
        objects.append(aux[0])
        performance.append(aux[1])

    plt.barh(yPos, performance, align='center', alpha=0.5)
    plt.yticks(yPos, objects)
    plt.xlabel('Frequency')
    plt.ylabel('Characters')
    plt.title('Character Frequency')
    plt.show()
