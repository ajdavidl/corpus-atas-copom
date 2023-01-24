import nltk
from nltk.collocations import *
import os

print("Loading data...")
AtasFolder = "../atas"
listAtas = os.listdir(AtasFolder)
corpus = []
for ata in listAtas:
    with open(AtasFolder + "/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines).lower()
            corpus.append(lines)

print(len(corpus), "minutes")

str_por = ' '.join(corpus)
str_por = str_por.lower()

tokens = nltk.wordpunct_tokenize(str_por)


# BIGRAMS
print("bigrams")
bigram_measures = nltk.collocations.BigramAssocMeasures()

finder_bigram = BigramCollocationFinder.from_words(tokens)
print(finder_bigram.nbest(bigram_measures.pmi, 10))

finder_bigram.apply_freq_filter(3)
print(finder_bigram.nbest(bigram_measures.pmi, 10))

scored_bigram = finder_bigram.score_ngrams(bigram_measures.raw_freq)
print(sorted(bigram for bigram, score in scored_bigram[:10]))

scored_bigram = finder_bigram.score_ngrams(bigram_measures.pmi)
print(sorted(bigram for bigram, score in scored_bigram[:10]))

#TRIGRAMS
print("trigrams")
trigram_measures = nltk.collocations.TrigramAssocMeasures()

finder_trigram = TrigramCollocationFinder.from_words(tokens)
print(finder_trigram.nbest(trigram_measures.pmi, 10))

finder_trigram.apply_freq_filter(3)
print(finder_trigram.nbest(trigram_measures.pmi, 10))

scored_trigram = finder_trigram.score_ngrams(trigram_measures.raw_freq)
print(sorted(trigram for trigram, score in scored_trigram[:10]))

scored_trigram = finder_trigram.score_ngrams(trigram_measures.pmi)
print(sorted(trigram for trigram, score in scored_trigram[:10]))
