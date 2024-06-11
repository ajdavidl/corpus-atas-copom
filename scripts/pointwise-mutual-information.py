import pandas as pd
import numpy as np
import re
import nltk
from collections import Counter
from random import sample
from load_texts import *  # return_data_frame() and Mystopwords

# CONFIG
JANELA_COOCORRENCIA = 5 # A janela será 2*x+1

print("Loading data...")
dfCorpus = return_data_frame()
dfCorpus.text = dfCorpus.text.apply(lambda x : x.lower())
corpus = dfCorpus.text.to_list()
print(len(corpus), "atas")

corpusJoined = ' '.join(corpus)
corpusSentences = nltk.tokenize.sent_tokenize(corpusJoined)
print("Number of sentences: ", len(corpusSentences))

def limpa_string(line):
    """Faz a limpeza da string removendo caracteres indesejados"""
    line = re.sub('[0-9]+', '_num_', line) #números
    line = re.sub('\n', '', line) #newline
    #line = re.sub(r'[^\w\s]','',line) #remove punctuation
    #line = re.sub('[\.!?,;:]','',line)
    line = re.sub('º','',line)
    line = re.sub('ª','',line)
    line = re.sub('@','',line)
    line = re.sub('=',' ',line)
    line = re.sub('#','',line)
    line = re.sub('\*','',line)
    line = re.sub('^-','',line) #retira travessão em início de frase
    line = re.sub('_',' ',line)
    line = re.sub('\|',' ',line)
    line = re.sub('«','',line)
    line = re.sub('»','',line)
    line = re.sub('_num_,_num_', '_num_', line) #números
    line = re.sub('_num_._num_', '_num_', line) #números
    line = re.sub('_num_/_num_', '_num_', line) #números
    return(line)

list_por = []
for line in corpusSentences:
    line = limpa_string(line)
    list_por.append(line)

list_por_tokens=[nltk.word_tokenize(list_por[i].lower()) for i in range(len(list_por))]

# CALCULANDO COOCORRÊNCIA DE PALAVRAS
print("coocorrência..")
list_coocur = []
dict_words = {}
dict_words_rev = {}
dict_words_freq = {}
for l in list_por_tokens:
    for i in range(len(l)):
        if l[i] not in dict_words_rev.keys():
            dict_words[ len(dict_words) ] = l[i]
            dict_words_rev[l[i]] = len(dict_words_rev)
            dict_words_freq[l[i]] = 1
        else:
            dict_words_freq[l[i]] = dict_words_freq[l[i]] + 1
        if i+JANELA_COOCORRENCIA >= len(l):
            rng = range(i+1,len(l))
        else:
            rng = range(i+1,i+JANELA_COOCORRENCIA)
        for j in rng:
            list_coocur.append( (l[i], l[j]) )

print("Número de pares: ", len(list_coocur))
print("Número de palavras: ", len(dict_words.keys()))

list(sorted(dict_words_freq.items(), key=lambda item: item[1], reverse=True))[:10]

dict_freq_coocur = Counter(list_coocur)

#PMI
print("PMI...")
tot_tup = sum(dict_freq_coocur.values())
tot = sum(dict_words_freq.values())

def PMI(tup):
    n = dict_freq_coocur[tup]
    n_x = dict_words_freq[tup[0]]
    n_y = dict_words_freq[tup[1]]
    if (n_x == 0) or (n_y == 0):
        return -np.inf
    return np.log((n/tot_tup)/((n_x/tot)*(n_y/tot)))

def NPMI(tup):
    n = dict_freq_coocur[tup]
    n_x = dict_words_freq[tup[0]]
    n_y = dict_words_freq[tup[1]]
    if (n_x == 0) or (n_y == 0) or (n == 0):
        return 0
    h = -np.log(n/tot_tup)
    pmi = np.log((n/tot_tup)/((n_x/tot)*(n_y/tot)))
    return min((pmi/h),1)



dict_PMI = {}
for t in dict_freq_coocur.keys():
    dict_PMI[t] = NPMI(t)

dict_inflacao = {}
dict_juros = {}

for t in dict_PMI.keys():
    if "inflação" in t:
        dict_inflacao[t] = dict_PMI[t]
    if "juros" in t:
        dict_juros[t] = dict_PMI[t]

print("tuplas com inflação:", len(dict_inflacao))
print("tuplas com juros:", len(dict_juros))

print("Maiores PMI com inflação")
print(list(sorted(dict_inflacao.items(), key=lambda item: item[1], reverse=True))[:10])
print()
print("Maiores PMI com juros")
print(list(sorted(dict_juros.items(), key=lambda item: item[1], reverse=True))[:10])