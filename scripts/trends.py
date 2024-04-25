import os
import re
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from collections import Counter


print("Loading data...")
AtasFolder = "../atas"
listAtas = os.listdir(AtasFolder)
listAtas = sorted(listAtas)
corpus = []
for ata in listAtas:
    with open(AtasFolder + "/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines).lower()
            corpus.append(lines)

print(len(corpus), "minutes")

for i in range(0, len(corpus)):
    corpus[i] = re.sub('\n', '', corpus[i])
    corpus[i] = re.sub('"', '', corpus[i])

dates = pd.read_csv("../copom_dates.csv")
minutes = dates.minute.values
dates = dates.publish_date.values

df = pd.DataFrame({"minute": minutes,
                   "date": dates,
                   "text": corpus})

df["date"] = pd.to_datetime(df["date"])
# print(df.info())


def create_df_ngrams(df_minutes):

    df_test = df_minutes[['date', 'text']].copy()
    df_test.columns = ['date', 'text']
    df_test['date'] = df_test['date'].apply(lambda x: x.date())

    df_test2 = df_test.groupby(['date'])['text'].apply(
        lambda x: ' '.join(x)).reset_index().sort_values(by='date')
    df_test2.set_index('date', inplace=True)
    df_test2['text'] = df_test2['text'].apply(lambda x: x.lower())
    df_test2['text'] = df_test2['text'].apply(lambda x: re.sub('\n', ' ', x))

    # df_test2 = df_test2.text.str.split(expand=True).stack().value_counts()

    print('COUNTING UNIGRAMS')

    i = df_test2.index[0]
    df_aux = df_test2.loc[[i]]['text'].str.split(
        expand=True).stack().value_counts().to_frame()
    df_aux.columns = ['qtt']
    df_aux['date'] = df_aux['qtt'].apply(lambda x: i)
    df_aux = df_aux.reset_index()
    df_aux.columns = ['word', 'qtt', 'date']

    for i in df_test2.index[1:]:
        df_aux2 = df_test2.loc[[i]]['text'].str.split(
            expand=True).stack().value_counts().to_frame()
        df_aux2.columns = ['qtt']
        df_aux2['date'] = df_aux2['qtt'].apply(lambda x: i)
        df_aux2 = df_aux2.reset_index()
        df_aux2.columns = ['word', 'qtt', 'date']
        df_aux = pd.concat([df_aux, df_aux2])

    # BIGRAMAS
    print('COUNTING BIGRAMS')

    i = df_test2.index[0]
    text = np.array2string(df_test2.loc[[i], ['text']].values)
    text = re.sub('\[', ' ', text)
    text = re.sub('\]', ' ', text)
    bigrams = [a+' '+b for l in [text]
               for a, b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
    bigrams = Counter(bigrams)
    df_aux2 = pd.DataFrame.from_dict(bigrams, orient='index').reset_index()
    df_aux2.columns = ['word', 'qtt']
    df_aux2 = df_aux2[df_aux2['word'] != ' ']
    df_aux2['date'] = df_aux2['qtt'].apply(lambda x: i)
    df_aux = pd.concat([df_aux, df_aux2])

    for i in df_test2.index[1:]:
        text = np.array2string(df_test2.loc[[i], ['text']].values)
        text = re.sub('\[', ' ', text)
        text = re.sub('\]', ' ', text)
        bigrams = [a+' '+b for l in [text]
                   for a, b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
        bigrams = Counter(bigrams)
        df_aux2 = pd.DataFrame.from_dict(bigrams, orient='index').reset_index()
        df_aux2.columns = ['word', 'qtt']
        df_aux2 = df_aux2[df_aux2['word'] != ' ']
        df_aux2['date'] = df_aux2['qtt'].apply(lambda x: i)
        df_aux = pd.concat([df_aux, df_aux2])

    # TRIGRAMAS
    print('COUNTING TRIGRAMS')

    i = df_test2.index[0]
    text = np.array2string(df_test2.loc[[i], ['text']].values)
    text = re.sub('\[', ' ', text)
    text = re.sub('\]', ' ', text)
    trigrams = [a+' '+b+' '+c for l in [text] for a, b,
                c in zip(l.split(" ")[:-2], l.split(" ")[1:-1], l.split(" ")[2:])]
    trigrams = Counter(trigrams)
    df_aux2 = pd.DataFrame.from_dict(trigrams, orient='index').reset_index()
    df_aux2.columns = ['word', 'qtt']
    df_aux2 = df_aux2[df_aux2['word'] != ' ']
    df_aux2['date'] = df_aux2['qtt'].apply(lambda x: i)
    df_aux = pd.concat([df_aux, df_aux2])

    for i in df_test2.index[1:]:
        text = np.array2string(df_test2.loc[[i], ['text']].values)
        text = re.sub('\[', ' ', text)
        text = re.sub('\]', ' ', text)
        trigrams = [a+' '+b+' '+c for l in [text] for a, b,
                    c in zip(l.split(" ")[:-2], l.split(" ")[1:-1], l.split(" ")[2:])]
        trigrams = Counter(trigrams)
        df_aux2 = pd.DataFrame.from_dict(
            trigrams, orient='index').reset_index()
        df_aux2.columns = ['word', 'qtt']
        df_aux2 = df_aux2[df_aux2['word'] != ' ']
        df_aux2['date'] = df_aux2['qtt'].apply(lambda x: i)
        df_aux = pd.concat([df_aux, df_aux2])

    df_final = df_aux.copy()

    del df_test, df_test2, df_aux, df_aux2, bigrams, trigrams

    # df_aux = df_final['date'].apply(
    #    lambda x: x.date()).value_counts().to_frame().reset_index()
    df_aux = df_final[['qtt', 'date']].groupby(
        'date').sum().reset_index()
    #df_aux = df_final['date'].value_counts().to_frame().reset_index()
    df_aux.columns = ['date', 'nr']
    df_final = df_final.merge(df_aux, how='left', on='date')
    df_final['index'] = df_final['qtt']/df_final['nr']
    del df_aux

    df_final = df_final[['word', 'date', 'index']]
    return(df_final)


df_trend = create_df_ngrams(df)


def plot_trends(df_ngrams, list_expressions, start_date=None, y_lim=None):
    """
    df_ngrams - data frame com a quantidade (indice) de expressoes por data
    lista_expressoes - lista de palavras, bigramas, trigramas para serem filtrados
    data de inicio dos gráficos no formato 'AAAA-MM-DD'
    y_lim - tupla com os limites do eixo y ex: (0, 1)
    """
    # plt.figure(figsize=(18, 16), dpi=80, facecolor='w', edgecolor='k')
    plt.rcParams.update({'font.size': 40})
    df_ngrams[df_ngrams['word'].str.contains('|'.join(list_expressions))].groupby('date').sum(
    ).sort_index().asfreq('D').dropna().plot(xlim=(start_date, np.max(df_trend['date'])), ylim=y_lim, linewidth=10)
    if type(list_expressions) == str:
        plt.title(list_expressions)
    else:
        plt.title(list_expressions[0])
    plt.show()


print(df_trend.info())
print(df_trend.sample(100))

df_trend['date'].value_counts().plot()
plt.show()

plot_trends(df_trend, 'juros')
plot_trends(df_trend, ['preço', 'preços'])
plot_trends(df_trend, ["câmbio", "dólar"])
plot_trends(df_trend, ["pib", "atividade"])
plot_trends(df_trend, "incerteza")
plot_trends(df_trend, "guerra")
plot_trends(df_trend, ["selic", "juros"])
plot_trends(df_trend, "taxa de juros")
plot_trends(df_trend, ["covid", "coronavírus", "pandemia"])
plot_trends(df_trend, "preços administrados")
plot_trends(df_trend, "livres")
plot_trends(df_trend, ["fiscal", "dívida líquida","dívida bruta","superávit primário"])
plot_trends(df_trend, "política monetária")
plot_trends(df_trend, "hiato")
plot_trends(df_trend, ["risco","riscos"])
plot_trends(df_trend, ["energia","bandeira","bandeiras","energética","energético"])
plot_trends(df_trend, ["focus","expectativa","expectativas"])
