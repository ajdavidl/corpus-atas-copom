import os
import re
import gensim

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy import linalg
from gensim.models import CoherenceModel, LdaModel, LsiModel, HdpModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition

from load_texts import return_data_frame, Mystopwords

print("loading texts ...")
df = return_data_frame()

corpus = df.text.to_list()

PARAGRAPHS = True

if PARAGRAPHS:
    corpusJoined = '\n'.join(corpus)
    corpusJoined = re.sub('\n \n', '\n', corpusJoined) 
    corpus = corpusJoined.split('\n')
    print(len(corpus), "paragraphs")

for i in range(0, len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub('\n', '', corpus[i])  # remove newline character
    corpus[i] = re.sub('[0-9]+', '', corpus[i])  # remove numbers
    corpus[i] = re.sub(r'[^\w\s]', '', corpus[i])  # remove punctuation
    corpus[i] = re.sub('\n', '', corpus[i])  # remove punctuation

Mystopwords = Mystopwords + ['aa','anterior','carlos','comitê','conforme','copom','dia','dias','doze','entanto','hoje','luiz','membros',
                             'mensal','monetária','otávio','pb','período','política','pp','quarto','relação','repectivamente','reunião','três',
                             'trimestre','trimestres']
# REMOVE STOPWORDS
for i in range(0, len(corpus)):
    words = corpus[i].split(" ")
    words_new = [w for w in words if w not in Mystopwords]
    corpus[i] = ' '.join(words_new)

count_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}',
                             ngram_range=(1, 1),
                             stop_words=Mystopwords,
                             #max_df = 10000,
                             min_df=100,
                             max_features=1000)
count_vect.fit(corpus)  # treina o objeto nos textos processados
count_vect_dtm = count_vect.transform(corpus)
count_vect_dtm.shape
vocab = np.array(count_vect.get_feature_names_out())

# Singular Value Decomposition (SVD)
print("\nSingular Value Decomposition (SVD)...")
U, s, Vh = linalg.svd(count_vect_dtm.todense(), full_matrices=False)
#print("U: ", U.shape, "\nS: ", s.shape, "\nVh: ", Vh.shape)

num_top_words = 5

def show_topics(a):
    def top_words(t): return [vocab[i]
                              for i in np.argsort(t)[:-num_top_words-1:-1]]
    topic_words = ([top_words(t) for t in a])
    return [' - '.join(t) for t in topic_words]


for topic in show_topics(Vh[:10]):
    print(topic)

# Truncated SVD
print("\nTruncated SVD ...")
Nr_topics = 10
svd_model = decomposition.TruncatedSVD(
    n_components=Nr_topics, algorithm='randomized', n_iter=100, random_state=122)
svd_model.fit(count_vect_dtm)

vocab = count_vect.get_feature_names_out()

for i, comp in enumerate(svd_model.components_):
    terms_comp = zip(vocab, comp)
    sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:7]
    print("\nTopic "+str(i)+": ")
    for t in sorted_terms:
        print('- '+t[0], end=' ')
print()

# Non-negative Matrix Factorization (NMF)
print("\nNon-negative Matrix Factorization (NMF)...")
Nr_topics = 10

clf = decomposition.NMF(n_components=Nr_topics, random_state=1)

W1 = clf.fit_transform(count_vect_dtm)
H1 = clf.components_

def get_nmf_topics(model, feat_names, num_topics):
    '''
    Model = trained model in NMF fit
    feat_names = word list from vectorizer.get_feature_names() vocabulary
    Nr_topics = number of topics
    '''
    # the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
    word_dict = {}
    for i in range(num_topics):
        # for each topic, obtain the largest values, and add the words they map to into the dictionary.
        words_ids = model.components_[i].argsort()[:-20 - 1:-1]
        words = [feat_names[key] for key in words_ids]
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = words
    return pd.DataFrame(word_dict)


print(get_nmf_topics(clf, vocab, Nr_topics))


# Latent Dirichlet Analysis (LDA)
print("\nLatent Dirichlet Analysis (LDA)...")

corpus2 = corpus.copy()
for idx in range(len(corpus2)):
    corpus2[idx] = [word for word in corpus2[idx].split(' ') if word not in ['']]


Nr_topics = 10
id2word = gensim.corpora.Dictionary(corpus2)
corpus_idx = [id2word.doc2bow(text) for text in corpus2]

lda = LdaModel(corpus=corpus_idx, id2word=id2word, num_topics=Nr_topics)


def get_topics(model, num_topics):
    word_dict = {}
    for i in range(num_topics):
        words = model.show_topic(i, topn=10)
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words]
    return pd.DataFrame(word_dict)


print(get_topics(lda, Nr_topics))


# Latent Semantic Indeixing (LSI)
print("\nLatent Semantic Indeixing (LSI)...")
lsi = LsiModel(corpus=corpus_idx, id2word=id2word, num_topics=Nr_topics)
print(get_topics(lsi, Nr_topics))

# Hierarchical Dirichlet process (HDP)
print("\nHierarchical Dirichlet process (HDP)...")
hdp = HdpModel(corpus=corpus_idx, id2word=id2word)
for topic in hdp.show_topics():
    print("topic:",topic[0])
    txt = topic[1]
    txt = re.sub('[0-9]+', '', txt)
    txt = re.sub(r'[^\w\s]', '', txt)
    print(txt)

# Topic Coherence
print("\nTopic Coherence...")

lsitopics = [[word for word, prob in topic]
             for topicid, topic in lsi.show_topics(formatted=False)]
hdptopics = [[word for word, prob in topic]
             for topicid, topic in hdp.show_topics(formatted=False)]
ldatopics = [[word for word, prob in topic]
             for topicid, topic in lda.show_topics(formatted=False)]

lsi_coherence = CoherenceModel(
    topics=lsitopics[:Nr_topics], texts=corpus, dictionary=id2word, window_size=10).get_coherence()
hdp_coherence = CoherenceModel(
    topics=hdptopics[:Nr_topics], texts=corpus, dictionary=id2word, window_size=10).get_coherence()
lda_coherence = CoherenceModel(
    topics=ldatopics, texts=corpus, dictionary=id2word, window_size=10).get_coherence()


def evaluate_bar_graph(coherences, indices):
    """
    Function to plot bar graph.
    coherences: list of coherence values
    indices: Indices to be used to mark bars. Length of this and coherences should be equal.
    """
    assert len(coherences) == len(indices)
    n = len(coherences)
    x = np.arange(n)
    plt.bar(x, coherences, width=0.2, tick_label=indices, align='center')
    plt.xlabel('Models')
    plt.ylabel('Coherence Value')
    plt.show()


evaluate_bar_graph([lsi_coherence, hdp_coherence, lda_coherence],
                   ['LSI', 'HDP', 'LDA'])
