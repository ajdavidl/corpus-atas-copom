import pandas as pd
import numpy as np
from load_texts import *  # return_data_frame() and Mystopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
import seaborn as sns
import matplotlib.pyplot as plt

from nltk.tokenize import word_tokenize
from gensim.models import FastText, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sentence_transformers import SentenceTransformer, util

df = return_data_frame()

print("TF-IDF")
vectorizer = TfidfVectorizer(
    stop_words=Mystopwords, analyzer='word', ngram_range=(1, 1),
    max_features=1000)
matrix = vectorizer.fit_transform(df.text.to_list())

matrix = matrix.todense()
terms = vectorizer.get_feature_names_out()
docs = df.index.values

df_vectors = pd.DataFrame(matrix, columns=terms, index=docs)

cos_sim = cosine_similarity(df_vectors)
print(cos_sim.shape)
pair_dist = pairwise_distances(df_vectors, metric='cosine')
print(pair_dist.shape)


nr_docs_to_show = 15
labels = [i for i in df.index[-nr_docs_to_show:]]

sns.heatmap(cos_sim[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Cosine similarity - TD-IDF")
plt.show()

sns.heatmap(pair_dist[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Pair wise distance - TF-IDF")
plt.show()


def similar_ata(nr_ata):
    print("similar docs to", nr_ata, ":")
    index_ata = nr_ata - 21
    col = cos_sim[:, index_ata]
    x = np.argsort(col, axis=-1)
    for i in x[-10:]:
        print(i+21)
    print()


similar_ata(255)
similar_ata(258)
similar_ata(100)

print("Doc2vec")
corpus = df.text.to_list()
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[
                              str(i)]) for i, _d in enumerate(corpus, start=21)]

max_epochs = 10
vec_size = 100
alpha = 0.025

model_D2V = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)

model_D2V.build_vocab(tagged_data)

for epoch in range(max_epochs):
    #print('iteration {0}'.format(epoch))
    model_D2V.train(
        tagged_data, total_examples=model_D2V.corpus_count, epochs=model_D2V.epochs)
    # decrease the learning rate
    model_D2V.alpha -= 0.0002
    # fix the learning rate, no decay
    model_D2V.min_alpha = model_D2V.alpha

vec = model_D2V.dv[0]
vec.shape = (1, vec_size)
df_vectors2 = pd.DataFrame(vec, columns=['V'+str(i) for i in range(vec_size)], index=[21])
for i in range(1, len(corpus)):
    vec = model_D2V.dv[i]
    vec.shape = (1, vec_size)
    df_aux = pd.DataFrame(vec, columns=['V'+str(j) for j in range(vec_size)], index=[i+21])
    df_vectors2 = pd.concat([df_vectors2, df_aux])


cos_sim2 = cosine_similarity(df_vectors2)
print(cos_sim2.shape)
pair_dist2 = pairwise_distances(df_vectors2, metric='cosine')
print(pair_dist2.shape)


nr_docs_to_show = 15
labels = [i for i in df.index[-nr_docs_to_show:]]

sns.heatmap(cos_sim2[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Cosine similarity doc2vec")
plt.show()

sns.heatmap(pair_dist2[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Pair wise distance doc2vec")
plt.show()

def similar_ata2(nr_ata):
    similar_doc = model_D2V.dv.most_similar(str(nr_ata))
    print("similar docs to "+str(nr_ata)+":")
    for word, sim in similar_doc:
        print(word, " -> {:.2f}".format(sim))
    print()

similar_ata2(250)
similar_ata2(258)
similar_ata2(100)

print("FastText")
corpus = df.text.to_list()
max_epochs = 10
vec_size = 100
model_FT = FastText(corpus, vector_size=vec_size,
                    window=3, min_count=1, epochs=max_epochs)


vec = model_FT.wv[ corpus[0] ]
vec.shape = (1, vec_size)
df_vectors3 = pd.DataFrame(vec, columns=['V'+str(i) for i in range(vec_size)], index=[21])
for i in range(1, len(corpus)):
    vec = model_FT.wv[ corpus[i] ]
    vec.shape = (1, vec_size)
    df_aux = pd.DataFrame(vec, columns=['V'+str(j) for j in range(vec_size)], index=[i+21])
    df_vectors3 = pd.concat([df_vectors3, df_aux])

cos_sim3 = cosine_similarity(df_vectors3)
print(cos_sim3.shape)
pair_dist3 = pairwise_distances(df_vectors3, metric='cosine')
print(pair_dist3.shape)


nr_docs_to_show = 15
labels = [i for i in df.index[-nr_docs_to_show:]]

sns.heatmap(cos_sim3[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Cosine similarity fastText")
plt.show()

sns.heatmap(pair_dist3[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Pair wise distance fastText")
plt.show()

def similar_ata3(nr_ata):
    print("similar docs to", nr_ata, ":")
    index_ata = nr_ata - 21
    col = cos_sim3[:, index_ata]
    x = np.argsort(col, axis=-1)
    for i in x[-10:]:
        print(i+21)
    print()


similar_ata3(255)
similar_ata3(258)
similar_ata3(100)

print("SBert")
corpus = df.text.to_list()
model_sbert = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
tensors = model_sbert.encode(corpus)
df_vectors4 = pd.DataFrame(tensors, index=range(21,len(corpus)+21))

cos_sim4 = cosine_similarity(df_vectors4)
print(cos_sim4.shape)
pair_dist4 = pairwise_distances(df_vectors4, metric='cosine')
print(pair_dist4.shape)


nr_docs_to_show = 15
labels = [i for i in df.index[-nr_docs_to_show:]]

sns.heatmap(cos_sim4[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Cosine similarity SBert")
plt.show()

sns.heatmap(pair_dist4[-nr_docs_to_show:, -nr_docs_to_show:],
            xticklabels=labels, yticklabels=labels)
plt.title("Pair wise distance SBert")
plt.show()

def similar_ata4(nr_ata):
    print("similar docs to", nr_ata, ":")
    index_ata = nr_ata - 21
    col = cos_sim4[:, index_ata]
    x = np.argsort(col, axis=-1)
    for i in x[-10:]:
        print(i+21)
    print()


similar_ata4(255)
similar_ata4(258)
similar_ata4(100)

def similar_ata_sbert(nr_ata):
    txt = corpus[nr_ata-21]
    queryTensor = model_sbert.encode(txt)
    similarities = util.cos_sim(queryTensor, tensors)
    similarities = similarities.argsort(descending=True).tolist()
    similarities = similarities[0][:10]
    listdocs = [i+21 for i in similarities]
    print("similar docs to", nr_ata, ":")
    for d in listdocs:
        print(d)
    print()

similar_ata_sbert(255)
similar_ata_sbert(258)
similar_ata_sbert(100)