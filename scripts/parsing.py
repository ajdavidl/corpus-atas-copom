import spacy
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
from collections import Counter

from load_texts import *  # return_data_frame() and Mystopwords

# Auxiliary functions
def formality(spacyDoc):
    ADJ = ADP = ADV = AUX = CONJ = CCONJ = DET = INTJ = NOUN = NUM = PART = 0
    PRON = PROPN = PUNCT = SCONJ = SYM = VERB = X = SPACE = 0
    for token in spacyDoc:
        pos = token.pos_
        if pos == 'NOUN':
            NOUN = NOUN + 1
        elif pos == 'ADP':
            ADP = ADP + 1
        elif pos == 'PUNCT':
            PUNCT = PUNCT + 1
        elif pos == 'DET':
            DET = DET + 1
        elif pos == 'VERB':
            VERB = VERB + 1
        elif pos == 'ADJ':
            ADJ = ADJ +1
        elif pos == 'PROPN':
            PROPN = PROPN + 1
        elif pos == 'NUM':
            NUM = NUM + 1
        elif pos == 'PRON':
            PRON = PRON + 1
        elif pos == 'ADV':
            ADV = ADV +1
        elif pos == 'AUX':
            AUX = AUX + 1
        elif pos == 'CONJ':
            CONJ = CONJ + 1
        elif pos == 'CCONJ':
            CCONJ = CCONJ + 1
        elif pos == 'INTJ':
            INTJ = INTJ + 1
        elif pos == 'PART':
            PART = PART + 1
        elif pos == 'SCONJ':
            SCONJ = SCONJ + 1
        elif pos == 'SYM':
            SYM = SYM + 1
        elif pos == 'X':
            X = X + 1
        elif pos == 'SPACE':
            SPACE = SPACE + 1
    F = NOUN + PROPN + ADJ + DET
    C = PRON + ADV + VERB + AUX + INTJ
    N = F + C + CONJ + CCONJ + SCONJ
    if N == 0:
        return (0)
    else:
        formality = 50 * ((F - C)/N + 1)
        return(formality)


def lexical_density(spacyDoc):
    ADJ = ADP = ADV = AUX = CONJ = CCONJ = DET = INTJ = NOUN = NUM = PART = 0
    PRON = PROPN = PUNCT = SCONJ = SYM = VERB = X = SPACE = 0
    for token in spacyDoc:
        pos = token.pos_
        if pos == 'NOUN':
            NOUN = NOUN + 1
        elif pos == 'ADP':
            ADP = ADP + 1
        elif pos == 'PUNCT':
            PUNCT = PUNCT + 1
        elif pos == 'DET':
            DET = DET + 1
        elif pos == 'VERB':
            VERB = VERB + 1
        elif pos == 'ADJ':
            ADJ = ADJ +1
        elif pos == 'PROPN':
            PROPN = PROPN + 1
        elif pos == 'NUM':
            NUM = NUM + 1
        elif pos == 'PRON':
            PRON = PRON + 1
        elif pos == 'ADV':
            ADV = ADV +1
        elif pos == 'AUX':
            AUX = AUX + 1
        elif pos == 'CONJ':
            CONJ = CONJ + 1
        elif pos == 'CCONJ':
            CCONJ = CCONJ + 1
        elif pos == 'INTJ':
            INTJ = INTJ + 1
        elif pos == 'PART':
            PART = PART + 1
        elif pos == 'SCONJ':
            SCONJ = SCONJ + 1
        elif pos == 'SYM':
            SYM = SYM + 1
        elif pos == 'X':
            X = X + 1
        elif pos == 'SPACE':
            SPACE = SPACE + 1
    N = ADJ + ADP + ADV + AUX + CONJ + CCONJ + DET + INTJ + NOUN + NUM + PART + PRON + PROPN + SCONJ + VERB
    if N == 0:
        return (0)
    else:
        lex_den = (NOUN + PROPN + ADJ + ADV + VERB + AUX)/N
        return(lex_den)    

# Main code

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
formality_ = []
lexical_density_ = []
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
    formality_.append(formality(doc))
    lexical_density_.append(lexical_density(doc))

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

X = dfCorpus.meeting.to_list()

plt.plot(X, formality_)
plt.title("Formality")
plt.xlabel("Meeting")
plt.ylabel("Formality")
plt.show()

plt.boxplot(formality_)
plt.title("Boxplot - Formality")
plt.show()

plt.plot(X, lexical_density_)
plt.title("Lexical Density")
plt.xlabel("Meeting")
plt.ylabel("Lexical Density")
plt.show()

plt.boxplot(lexical_density_)
plt.title("Boxplot - lexical_density")
plt.show()