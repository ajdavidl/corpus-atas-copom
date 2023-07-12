import pandas as pd
import re
import nltk
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE, MDS
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import matplotlib.cm as cm
from collections import Counter

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
corpusJoined = corpusJoined.lower()
for i in range(0, len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub('\n', '', corpus[i])  # remove newline character

Mystopwords = ['ainda', 'ante', 'p', 'r', 'sobre'] + ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',
                                                      'outubro', 'novembro', 'dezembro', 'mês', 'meses', 'ano', 'anos'] + [str(i) for i in range(10)] + nltk.corpus.stopwords.words('portuguese')


# REMOVE STOPWORDS
for i in range(0, len(corpus)):
    words = corpus[i].split(" ")
    words_new = [w for w in words if w not in Mystopwords]
    corpus[i] = ' '.join(words_new)

# TF-IDF
print("Calculating TF-IDF...")
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}',
                             ngram_range=(1, 3),
                             stop_words=Mystopwords,
                             #max_df = 10000,
                             # min_df=100,
                             max_features=1000)
tfidf_vect_dtm = tfidf_vect.fit_transform(corpus)
print(tfidf_vect_dtm.shape)
dist_tfidf = 1 - cosine_similarity(tfidf_vect_dtm)
terms_tfidf = tfidf_vect.get_feature_names_out()

print("Visualizing data with TSNE")
tfidf_embedded = TSNE(n_components=2).fit_transform(tfidf_vect_dtm.toarray())

sns.scatterplot(x=tfidf_embedded[:, 0], y=tfidf_embedded[:, 1])
plt.title('DTM - TFIDF')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# K-means clustering
print("K-means...")
num_clusters = 5
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_vect_dtm)
clusters = km.labels_.tolist()

print(Counter(clusters))

# Multi-dimensional Scaling (MDS)
mds = MDS(n_components=5, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist_tfidf)  # shape (n_components, n_samples)
xs, ys = pos[:, 0], pos[:, 1]

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
for i in range(num_clusters):
    terms = []
    print("cluster: ", i)
    for ind in order_centroids[i, :10]:
        terms.append(terms_tfidf[ind])
    print(terms)

cluster_colors = {0: '#1b9e77', 1: '#d95f02',
                  2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#0fffff'}

# set up cluster names using a dict
cluster_names = {x: str(x) for x in range(num_clusters)}

minute = [n for n in range(21, len(clusters)+21)]

# create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(minute=minute, x=xs, y=ys, label=clusters))

print(df[['minute', 'label']])
# group by cluster
groups = df.groupby('label')

# set up plot
fig, ax = plt.subplots(figsize=(17, 9))  # set size
ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling

# iterate through groups to layer the plot
# note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
            label=cluster_names[name], color=cluster_colors[name], mec='none')
    ax.set_aspect('auto')
    ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(
        axis='y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')

ax.legend(numpoints=1)  # show legend with only 1 point

plt.show()  # show the plot

colors = cm.rainbow(np.linspace(0, 1, num_clusters))

for i in range(num_clusters):
    aux = df[df.label == i]
    plt.scatter(aux['x'].tolist(), aux['y'].tolist(), color=colors[i])
plt.show()

# Hierarchical documetn clustering
print("Hierarchical clustering")
# define the linkage_matrix using ward clustering pre-computed distances
linkage_matrix = ward(dist_tfidf)

fig, ax = plt.subplots(figsize=(15, 20))  # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=minute)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout()  # show plot with tight layout
plt.show()
