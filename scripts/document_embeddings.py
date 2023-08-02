# Documents embeddings using TFIDF vectors

import pandas as pd
import numpy as np
from load_texts import *  # return_data_frame() and Mystopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances

df = return_data_frame()

vectorizer = TfidfVectorizer(
    stop_words=Mystopwords, analyzer='word', ngram_range=(1, 1),
    max_features=1000)
matrix = vectorizer.fit_transform(df.text.to_list())

matrix = matrix.todense()
terms = vectorizer.get_feature_names_out()
docs = df.index.values

print(matrix.shape)
print(terms.shape)
print(docs.shape)

df_vectors = pd.DataFrame(matrix, columns=terms, index=docs)
print(df_vectors.info())
print(df_vectors.sample(2))

cos_sim = cosine_similarity(df_vectors)
print(cos_sim.shape)
pair_dist = pairwise_distances(df_vectors, metric='cosine')
print(pair_dist.shape)


def similar_ata(nr_ata):
    print("similar docs to", nr_ata, ":")
    index_ata = nr_ata - 21
    col = cos_sim[:, index_ata]
    x = np.argsort(col, axis=-1)
    for i in x[-10:]:
        print(i+21)
    print()


similar_ata(255)

similar_ata(250)

similar_ata(100)
