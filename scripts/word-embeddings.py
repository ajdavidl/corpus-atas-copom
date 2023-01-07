import numpy as np
import pandas as pd
import re
import os
from sklearn.decomposition import PCA
from gensim.models import Word2Vec, FastText, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

print("Loading data...")
AtasFolder = "../atas"
listAtas = os.listdir(AtasFolder)
corpus = []
meeting = []
for ata in listAtas:
    meeting.append(int(re.search("[0-9]+", ata).group()))
    with open(AtasFolder + "/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines).lower()
            corpus.append(lines)

print(len(corpus), "atas")
dfCorpus = pd.DataFrame(corpus, index=meeting, columns=["corpus"])
del meeting


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
print('\n', "Word2vec")

sentences = [word_tokenize(sent) for sent in corpus]
model_W2V = Word2Vec(sentences, min_count=1)
model_W2V.train(sentences, total_examples=len(sentences), epochs=100)

analogy(model_W2V, 'ipca', 'inflação', 'selic')
display_pca_scatterplot(model_W2V,
                        ['selic', 'inflação', 'ipca', 'juros', 'pib', 'dólar', 'câmbio'])


def W2Vsimilarity(word):
    print('\n', 'Similar to ', word, ":")
    similars = model_W2V.wv.similar_by_word(word, 10)
    for word, sim in similars:
        print(word, " -> {:.2f}".format(sim))


W2Vsimilarity('atividade')
W2Vsimilarity('ipca')
W2Vsimilarity('selic')

# # Doc2Vec
print('\n', "Doc2vec")
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
D2Vsimilarity('ipca')
D2Vsimilarity('juros')

display_pca_scatterplot(model_D2V,
                        ['selic', 'inflação', 'ipca', 'juros', 'pib', 'dólar', 'câmbio'])

# # FastText
print('\n', "FastText")
model_FT = FastText(sentences, vector_size=100,
                    window=3, min_count=1, epochs=10)


def FTsimilar(word):
    print('\n', 'Similar to ', word)
    similars = model_FT.wv.most_similar(positive=[word])
    for word, sim in similars:
        print(word, " -> {:.2f}".format(sim))


analogy(model_FT, 'ipca', 'inflação', 'selic')
FTsimilar('inflação')
FTsimilar('selic')
FTsimilar('ipca')

analogy(model_FT, 'selic', 'ipca', 'juros')

#model_FT.wv.doesnt_match("selic pib ipca crise".split())
#
#model_FT.wv.doesnt_match("alto baixo aumento ipca".split())
#
#model_FT.wv.similarity('selic', 'ipca')

display_pca_scatterplot(model_FT, sample=20)

display_pca_scatterplot(model_FT,
                        ['selic', 'inflação', 'ipca', 'juros', 'pib', 'dólar', 'câmbio'])
