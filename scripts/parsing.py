import spacy
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
from collections import Counter

from load_texts import *  # return_data_frame() and Mystopwords

print("Loading data...")
dfCorpus = return_data_frame()
dfCorpus.text = dfCorpus.text.apply(lambda x : x.lower())
corpus = dfCorpus.text.to_list()
print(len(corpus), "minutes")

for i in range(0, len(corpus)):
    corpus[i] = re.sub('\n', '', corpus[i])
    corpus[i] = re.sub('"', '', corpus[i])

nlp = spacy.load('pt_core_news_sm')

print("Parsing texts...")
text = []
pos = []
tag = []
dep = []
ent_text = []
ent_label = []
for sentence in corpus:
    doc = nlp(sentence)
    for token in doc:
        text.append(token.text)
        pos.append(token.pos_)
        tag.append(token.tag_)
        dep.append(token.dep_)
    for ent in doc.ents:
        ent_text.append(ent.text)
        ent_label.append(ent.label_)

df = pd.DataFrame(list(zip(text, pos)),
                  columns=['word', 'pos'])

print("Making plots...")
# NOUNS
df[(df['pos'] == 'PROPN') | (df['pos'] == 'NOUN')
   ].loc[:, 'word'].value_counts()[:20].plot.bar(rot=45, title="Nouns")
plt.show()

# ADJECTIVES
df[df['pos'] == 'ADJ'].loc[:, 'word'].value_counts()[:20].plot.bar(rot=45,
                                                                   title="Adjectives")
plt.show()

# VERBS
df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')].loc[:,
                                                     'word'].value_counts()[:20].plot.bar(rot=45, title="Verbs")
plt.show()

# ADVERBS
df[df['pos'] == 'ADV'].loc[:, 'word'].value_counts()[:20].plot.bar(rot=45,
                                                                   title="Adverbs")
plt.show()

# CONJUNCTIONS
df[(df['pos'] == 'CONJ') | (df['pos'] == 'CCONJ') | (df['pos'] == 'SCONJ')
   ].loc[:, 'word'].value_counts()[:10].plot.bar(rot=45, title="Conjunctions")
plt.show()

# Punctuation
df[df['pos'] == 'PUNCT'].loc[:, 'word'].value_counts()[:5].plot.bar(rot=45,
                                                                    title="Punctuation")
plt.show()

# Interjection
#df[df['pos'] == 'INTJ'].loc[:,'word'].value_counts()[:10].plot.bar(rot=45, title = "Interjections")
# plt.show()

# Determiner
df[df['pos'] == 'DET'].loc[:, 'word'].value_counts()[:10].plot.bar(rot=45,
                                                                   title="Determiners")
plt.show()

# Pronouns
df[df['pos'] == 'PRON'].loc[:, 'word'].value_counts()[:10].plot.bar(rot=45,
                                                                    title="Pronouns")
plt.show()

# Numerals
df[df['pos'] == 'NUM'].loc[:, 'word'].value_counts()[:10].plot.bar(rot=45,
                                                                   title="Numerals")
plt.show()

# Symbols
df[df['pos'] == 'SYM'].loc[:, 'word'].value_counts()[:5].plot.bar(rot=45,
                                                                  title="Symbols")
plt.show()

# POS tags
D = Counter(pos)
print(D)
plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), list(D.keys()), rotation=45)
plt.title("POS")
plt.show()


# tags
D = {x: y for x, y in Counter(tag).most_common(10)}
plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), list(D.keys()), rotation=45)
plt.title("tags")
plt.show()

# Dependencies
D = {x: y for x, y in Counter(dep).most_common(15)}
plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), list(D.keys()), rotation=45)
plt.title("Dependencies")
plt.show()

# Entities
# convert list of tuples in dictionary
D = {x: y for x, y in Counter(ent_text).most_common(15)}
plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), list(D.keys()), rotation=45)
plt.title("Entities")
plt.show()

# Entities labels
D = Counter(ent_label)
plt.bar(range(len(D)), list(D.values()),
        align='center')
plt.xticks(range(len(D)), list(D.keys()), rotation=45)
plt.title("Entities labels")
plt.show()
