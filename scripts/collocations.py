import nltk
from nltk.collocations import *

from load_texts import read_text_files

print("Loading data...")
corpus = read_text_files()[0]
print(len(corpus), "minutes")

str_por = ' '.join(corpus)
str_por = str_por.lower()

tokens = nltk.wordpunct_tokenize(str_por)

def print_collocations(finder):
    """
    finder : list of tuples
    """
    count = 1
    for tup in finder:
        print(count,")", sep='', end=' ')
        for word in tup:
            print(word, end=' ')
        print()
        count+=1

freq = 100
nr_coll = 100
# BIGRAMS
print("\nBIGRAMS COLLOCATIONS")
bigram_measures = nltk.collocations.BigramAssocMeasures()

print("Bigrams - nbest - pmi")
finder_bigram = BigramCollocationFinder.from_words(tokens)
print_collocations(finder_bigram.nbest(bigram_measures.pmi, nr_coll))
print()

print("Bigrams - nbest - pmi - min freq:", freq)
finder_bigram.apply_freq_filter(freq)
print_collocations(finder_bigram.nbest(bigram_measures.pmi, nr_coll))
print()

print("Bigrams - score_ngrams - raw_freq - min freq:", freq)
scored_bigram = finder_bigram.score_ngrams(bigram_measures.raw_freq)
print_collocations(sorted(bigram for bigram, score in scored_bigram[:nr_coll]))
print()

print("Bigrams - score_ngrams - pmi - min freq:", freq)
scored_bigram = finder_bigram.score_ngrams(bigram_measures.pmi)
print_collocations(sorted(bigram for bigram, score in scored_bigram[:nr_coll]))
print()

#TRIGRAMS
print("\nTRIGRAMS COLLOCATIONS")
trigram_measures = nltk.collocations.TrigramAssocMeasures()

print("Trigrams - nbest - pmi")
finder_trigram = TrigramCollocationFinder.from_words(tokens)
print_collocations(finder_trigram.nbest(trigram_measures.pmi, nr_coll))
print()

print("Trigrams - nbest - pmi - min freq:", freq)
finder_trigram.apply_freq_filter(freq)
print_collocations(finder_trigram.nbest(trigram_measures.pmi, nr_coll))
print()

print("Trigrams - score_ngrams - raw_freq - min freq:", freq)
scored_trigram = finder_trigram.score_ngrams(trigram_measures.raw_freq)
print_collocations(sorted(trigram for trigram, score in scored_trigram[:nr_coll]))
print()

print("Trigrams - score_ngrams - pmi - min freq:", freq)
scored_trigram = finder_trigram.score_ngrams(trigram_measures.pmi)
print_collocations(sorted(trigram for trigram, score in scored_trigram[:nr_coll]))
print()

