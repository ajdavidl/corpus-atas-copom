import os
import re
import nltk
import pandas as pd
import numpy as np

Mystopwords = ['ainda', 'ante', 'desde', 'enquanto', 'p', 'r', 'sobre',
'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',  'outubro', 'novembro', 'dezembro', 'mês', 'meses', 'ano', 'anos'] + [str(i) for i in range(10)] + nltk.corpus.stopwords.words('portuguese')


def read_text_files():
    listAtas = os.listdir("../atas")
    corpus = []
    meeting = []
    for ata in listAtas:
        meeting.append(int(re.search("[0-9]+", ata).group()))
        with open("../atas/" + ata, 'rt', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                lines = ' '.join(lines)
                corpus.append(lines)
    return [corpus, meeting]


def return_data_frame():
    corpus, meeting = read_text_files()
    dfCorpus = pd.DataFrame(corpus, index=meeting, columns=["text"])
    del corpus, meeting
    decisions = pd.read_csv("../decisions.csv")
    decisions = decisions.dropna()
    dfAux = decisions[decisions.meeting == 45]
    decisions = decisions.drop(dfAux.index[1])
    decisions.index = np.int64(decisions.meeting.values)
    dfCorpus = dfCorpus.join(decisions)
    dates = pd.read_csv("../copom_dates.csv")
    dates.index = dates.minute
    dfCorpus = dfCorpus.join(dates)
    dfCorpus = dfCorpus.sort_index()
    return dfCorpus
