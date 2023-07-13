import pandas as pd
import tomotopy as tp
import re
import os
import nltk
from collections import Counter

Mystopwords = ['ainda', 'ante', 'p', 'r', 'sobre'] + ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',
                                                      'outubro', 'novembro', 'dezembro', 'mês', 'meses', 'ano', 'anos'] + [str(i) for i in range(10)] + nltk.corpus.stopwords.words('portuguese')
Mystopwords = Mystopwords + ["inflação", "economia", "juros", "taxa", "comitê", "copom", "anterior",
                             "preços", "preço", "política", "monetária", "pp", "doze", "meses"]

print("loading texts ...")
listAtas = os.listdir("../atas")

corpus = []

for ata in listAtas:
    with open("../atas/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines)
            corpus.append(lines)

print("Cleaning texts ...")

for i in range(len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub('[0-9]+', '', corpus[i])  # remove numbers
    corpus[i] = re.sub(r'[^\w\s]', '', corpus[i])  # remove punctuation
    corpus[i] = re.sub('\n', '', corpus[i])  # remove \n - newline


# REMOÇÃO DE STOP WORDS
for i in range(0, len(corpus)):  # varre a lista de textos
    words = corpus[i].split(" ")  # separa o texto em palavras
    # remove as stop words
    words_new = [w for w in words if w not in Mystopwords]
    corpus[i] = ' '.join(words_new)  # concantena as palavras novamente


#corpus_hlda = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer(), stopwords=lambda x: len(x) <= 2 or x in Mystopwords)
#corpus_hlda = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer(), stopwords=Mystopwords)
corpus_hlda = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer())
corpus_hlda.process(corpus)


print("Training...")
mdl = tp.HLDAModel(tw=tp.TermWeight.ONE,
                   min_cf=10,
                   min_df=4,
                   # rm_top=0,
                   depth=4,
                   alpha=0.3, eta=0.01, gamma=0.1,  # seed=None,
                   corpus=corpus_hlda,
                   transform=None)

mdl.train(0)
print(len(mdl.used_vocabs))

print('Num docs:', len(mdl.docs), ', Vocab size:', len(
    mdl.used_vocabs), ', Num words:', mdl.num_words)
print('Removed top words:', mdl.removed_top_words)
for i in range(0, 5000, 10):
    mdl.train(10, workers=6)
    print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

print(mdl.depth)

for k in range(mdl.k):
    if not mdl.is_live_topic(k):
        continue
    print('Topic #{}'.format(k))
    print('Level', mdl.level(k))
    print('Alive', mdl.is_live_topic(k))
    print('Nr Docs:', mdl.num_docs_of_topic(k))
    print('Parent Topics:')
    print(mdl.parent_topic(k))
    print('Children Topics:')
    print(mdl.children_topics(k))
    for word, prob in mdl.get_topic_words(k):
        print('\t', word, prob, sep='\t')

hlda_topics = []
for i in range(len(mdl.docs)):
    hlda_topics.append(mdl.docs[i].path[-1])
    #print(i+21, '-', hlda_topics[-1])

print(Counter(hlda_topics))
