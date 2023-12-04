import re
import nltk
import os
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import numpy as np
import wordcloud

from load_texts import *  # return_data_frame() and Mystopwords

print("Loading data...")
dfCorpus = return_data_frame()
dfCorpus.text = dfCorpus.text.apply(lambda x : x.lower())
corpus = dfCorpus.text.to_list()
print(len(corpus), "minutes")

corpusJoined = ' '.join(corpus)
corpusJoined = corpusJoined.lower()
for i in range(0, len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub('\n', '', corpus[i])  # remove newline character

def frequencyPlot(listText, number_of_words=20, stopwords=None, ngramRange=(1, 1), vocabulary=None):
    count_vect = CountVectorizer(
        analyzer='word',
        stop_words=stopwords,
        ngram_range=ngramRange,
        vocabulary=vocabulary
    )
    count_vect.fit(listText)
    bag_of_words = count_vect.transform(listText)
    sum_words = bag_of_words.sum(axis=0)
    word_freq = [(word, sum_words[0, idx])
                 for word, idx in count_vect.vocabulary_.items()]
    word_freq = sorted(word_freq, key=lambda x: x[1], reverse=True)
    yPos = np.arange(number_of_words)
    objects = []
    performance = []
    for i in range(number_of_words):
        aux = word_freq[i]
        objects.append(aux[0])
        performance.append(aux[1])
    plt.barh(yPos, performance, align='center', alpha=0.5)
    plt.yticks(yPos, objects)
    plt.xlabel('Frequency')
    plt.ylabel('Tokens')
    plt.title('Frequency of tokens')
    plt.show()


def wordcloudPlot(text, stopwords=None, max_font_size=50, max_words=100, background_color="white"):
    cloud = wordcloud.WordCloud(stopwords=stopwords, max_font_size=max_font_size,
                                max_words=max_words, background_color=background_color).generate(text.lower())

    # Display the generated image:
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


numberOfWords = 20

print("Word frequencies with stop words")
frequencyPlot(corpus, numberOfWords, stopwords=None, ngramRange=(1, 1))
wordcloudPlot(corpusJoined, stopwords=None)

print("Word frequencies without stop words")
frequencyPlot(corpus, numberOfWords, stopwords=Mystopwords, ngramRange=(1, 1))
wordcloudPlot(corpusJoined, stopwords=Mystopwords)

print("Bigram frequencies with stop words")
frequencyPlot(corpus, numberOfWords, stopwords=None, ngramRange=(2, 2))

print("Bigram frequencies without stop words")
frequencyPlot(corpus, numberOfWords, stopwords=Mystopwords, ngramRange=(2, 2))

print("Trigram frequencies with stop words")
frequencyPlot(corpus, numberOfWords, stopwords=None, ngramRange=(3, 3))

print("Trigram frequencies without stop words")
frequencyPlot(corpus, numberOfWords, stopwords=Mystopwords, ngramRange=(3, 3))
