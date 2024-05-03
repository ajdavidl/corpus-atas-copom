import numpy as np
import pandas as pd
import re
import os
from sklearn.decomposition import PCA
from gensim.models import Word2Vec, FastText, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

from load_texts import *  # return_data_frame() and Mystopwords

print("Loading data...")
dfCorpus = return_data_frame()
dfCorpus.text = dfCorpus.text.apply(lambda x : x.lower())
corpus = dfCorpus.text.to_list()
print(len(corpus), "atas")

for i in range(0, len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub('\n', '', corpus[i])  # remove newline character
    corpus[i] = re.sub('[0-9]+', '', corpus[i])  # remove numbers
    corpus[i] = re.sub(r'[^\w\s]', ' ', corpus[i])  # remove punctuation
    

def display_pca_scatterplot(model, words=None, sample=0):
    if words == None:
        if sample > 0:
            words = np.random.choice(
                list(model.wv.key_to_index.keys()), sample)
        else:
            words = [word for word in model.wv.vocab]
    word_vectors = np.array([model.wv[w]
                            for w in words if w in model.wv.key_to_index])
    twodim = PCA().fit_transform(word_vectors)[:, :2]
    plt.figure(figsize=(6, 6))
    plt.scatter(twodim[:, 0], twodim[:, 1], edgecolors='k', c='r')
    for word, (x, y) in zip(words, twodim):
        plt.text(x+0.05, y+0.05, word)
    plt.show()


def analogy(model, x1, x2, y1):
    result = model.wv.most_similar(positive=[y1, x2], negative=[x1])
    print("\n", y1, " + ", x2, " - ", x1, " = ", result[0][0])


# # Word2Vec
print('\n', "Word2vec -----------------------------------------------")

sentences = [word_tokenize(sent) for sent in corpus]
model_W2V = Word2Vec(sentences, min_count=1)
model_W2V.train(sentences, total_examples=len(sentences), epochs=100)

analogy(model_W2V, 'ipca', 'inflação', 'selic')
analogy(model_W2V, 'ipca', 'inflação', 'dólar')
analogy(model_W2V, 'dólar', 'câmbio', 'selic')
display_pca_scatterplot(model_W2V,
                        ['selic', 'inflação', 'ipca', 'juros', 'pib', 'dólar', 'câmbio'])


def W2Vsimilarity(word):
    print('\n', 'Similar to ', word, ":")
    similars = model_W2V.wv.similar_by_word(word, 10)
    for word, sim in similars:
        print(word, " -> {:.2f}".format(sim))


W2Vsimilarity('atividade')
W2Vsimilarity('desemprego')
W2Vsimilarity('hiato')
W2Vsimilarity('fiscal')
W2Vsimilarity('ipca')
W2Vsimilarity('inflação')
W2Vsimilarity('administrados')
W2Vsimilarity('livres')
W2Vsimilarity('selic')
W2Vsimilarity('juros')
W2Vsimilarity('dólar')
W2Vsimilarity('câmbio')

# # Doc2Vec
print('\n', "Doc2vec -----------------------------------------------")
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

similar_doc = model_D2V.dv.most_similar('250')
for word, sim in similar_doc:
    print(word, " -> {:.2f}".format(sim))


def D2Vsimilarity(word):
    print('\n', 'Similar to ', word)
    similars = model_D2V.wv.similar_by_word(word, 10)
    for word, sim in similars:
        print(word, " -> {:.2f}".format(sim))


analogy(model_D2V, 'ipca', 'inflação', 'selic')
analogy(model_D2V, 'ipca', 'inflação', 'dólar')
analogy(model_D2V, 'dólar', 'câmbio', 'selic')

D2Vsimilarity('atividade')
D2Vsimilarity('desemprego')
D2Vsimilarity('hiato')
D2Vsimilarity('fiscal')
D2Vsimilarity('ipca')
D2Vsimilarity('inflação')
D2Vsimilarity('administrados')
D2Vsimilarity('livres')
D2Vsimilarity('selic')
D2Vsimilarity('juros')
D2Vsimilarity('dólar')
D2Vsimilarity('câmbio')

display_pca_scatterplot(model_D2V,
                        ['selic', 'inflação', 'ipca', 'juros', 'pib', 'dólar', 'câmbio'])


# Doc2Vec heatmap
length = 10
x1 = int(dfCorpus.meeting.to_list()[-1])
x0 = x1 - length
matrix = np.zeros((length, length))
for i in range(length):
    for j in range(length):
        matrix[i,j] = model_D2V.dv.distance( str(x0+i+1) , str(x0+j+1) )
fig, ax = plt.subplots()
im = ax.imshow(matrix)
# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(length), labels=[str(x0+i+1) for i in range(length)])
ax.set_yticks(np.arange(length), labels=[str(x0+i+1) for i in range(length)])
# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
# Loop over data dimensions and create text annotations.
for i in range(length):
    for j in range(length):
        text = ax.text(j, i, round(matrix[i, j],1),
                       ha="center", va="center", color="w")
ax.set_title("Distance between minutes")
fig.tight_layout()
plt.show()



# # FastText
print('\n', "FastText -----------------------------------------------")
model_FT = FastText(sentences, vector_size=100,
                    window=3, min_count=1, epochs=10)


def FTsimilarity(word):
    print('\n', 'Similar to ', word)
    similars = model_FT.wv.most_similar(positive=[word])
    for word, sim in similars:
        print(word, " -> {:.2f}".format(sim))


analogy(model_FT, 'ipca', 'inflação', 'selic')
analogy(model_FT, 'ipca', 'inflação', 'dólar')
analogy(model_FT, 'dólar', 'câmbio', 'selic')

FTsimilarity('atividade')
FTsimilarity('desemprego')
FTsimilarity('hiato')
FTsimilarity('fiscal')
FTsimilarity('ipca')
FTsimilarity('inflação')
FTsimilarity('administrados')
FTsimilarity('livres')
FTsimilarity('selic')
FTsimilarity('juros')
FTsimilarity('dólar')
FTsimilarity('câmbio')

analogy(model_FT, 'selic', 'ipca', 'juros')

#model_FT.wv.doesnt_match("selic pib ipca crise".split())
#
#model_FT.wv.doesnt_match("alto baixo aumento ipca".split())
#
#model_FT.wv.similarity('selic', 'ipca')

display_pca_scatterplot(model_FT, sample=20)

display_pca_scatterplot(model_FT,
                        ['selic', 'inflação', 'ipca', 'juros', 'pib', 'dólar', 'câmbio'])
