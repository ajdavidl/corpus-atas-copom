import re
import spacy
import scattertext as st
from load_texts import *  

nlp = spacy.load('pt_core_news_sm')

PT_BR = False

def removeNumbers(string):
    if type(string)!=str:
        return(string)
    string = re.sub('[0-9]+','',string)
    return(string)

print('loading texts...')
df = return_data_frame()
print(df.shape[0], "minutes")

Mystopwords = Mystopwords + ['acordar', 'agora', 'ainda', 'aladi', 'alegrar', 'além', 'antar', 'ante', 'anthero', 'antonio', 'apenas', 'apesar', 'apresentação', 'aquém', 'araújo', 'cada', 'capitar', 'carioca', 'carteiro', 'contra', 'corpus', 'corrêa', 'costa', 'daquela', 'demais', 'diante', 'edson', 'entanto', 'estar', 'estevar', 'então', 'feltrim', 'final', 'finar', 'geral', 'içar', 'ie', 'intuito'] + \
    ['le', 'luiz', 'luzir', 'mediante', 'meirelles', 'mercar', 'moraes', 'necessariamente', 'neto', 'of', 'oficiar', 'oliveira', 'onde', 'ora', 'parir', 'paulo', 'pelar', 'pesar', 'pilar', 'pois', 'primo', 'quadrar', 'reinar', 'res', 'resinar', 'reunião', 'ser', 'sob', 'sobre', 'somente', 'sr', 'tal', 'tais', 'tanto', 'thomson', 'tipo', 'todo', 'tony', 'usecheque', 'vasconcelos'] + \
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] + \
    ['um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove', 'vinte'] + \
    ['aquela', 'aquelas', 'aquele', 'aqueles', 'àquela', 'àquelas', 'daquele', 'daqueles', 'daquela', 'daquelas', 'naquele', 'naqueles', 'naquela', 'naquelas', 'neste', 'nesta', 'nestes', 'nestas', 'nisto', 'nesse', 'nessa', 'nesses', 'nessas', 'nisso',
    'desse', 'dessa', 'desses', 'dessas', 'disso','fins','meados','mencionado','modo','última','fgv','tende','torno','diz'] + \
    ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro',
        'dezembro', 'mês', 'meses', 'ano', 'anos','hoje', 'reuniões','ciclo'] + \
    ["banco","central","copom","doze","membros","meses","os","se","dessa",]
Mystopwords = set(Mystopwords)

corpus = df['text'].to_list()

if PT_BR:
    keep = "manutenção"
    lower = "redução"
    raise_ = "aumento"
    decisions = df['decision'].to_list()
    for i,d in enumerate(decisions):
        if d == 'lower':
            decisions[i] = 'redução'
        elif d == 'raise':
            decisions[i] = 'aumento'
        elif d == 'keep':
            decisions[i] = 'manutenção'
        else:
            print('Error in index:', i)
    df['decision'] = decisions
else:
    keep = "keep"
    lower = "lower"
    raise_ = "raise"

for i in range(len(corpus)):
    corpus[i] = removeNumbers(corpus[i])
df['text_clean'] = corpus

print("Doing lower X raise")
lowerXraise = st.CorpusFromPandas(df[df['decision'].isin([lower,raise_])],
                             category_col='decision',
                             text_col='text_clean',
                             nlp=nlp).build().remove_terms(Mystopwords, ignore_absences=True)

html = st.produce_scattertext_explorer(lowerXraise,
                                       category=lower,
                                       category_name=lower,
                                       not_category_name=raise_,
                                       width_in_pixels=1000,
                                       )
open("raise_x_lower.html", 'wb').write(html.encode('utf-8'))

print("Doing lower X keep")
lowerXkeep = st.CorpusFromPandas(df[df['decision'].isin([lower,keep])],
                             category_col='decision',
                             text_col='text_clean',
                             nlp=nlp).build().remove_terms(Mystopwords, ignore_absences=True)

html2 = st.produce_scattertext_explorer(lowerXkeep,
                                       category=lower,
                                       category_name=lower,
                                       not_category_name=keep,
                                       width_in_pixels=1000,
                                       )
open("keep_x_lower.html", 'wb').write(html2.encode('utf-8'))

print("Doing raise X keep")
keepXraise = st.CorpusFromPandas(df[df['decision'].isin([raise_,keep])],
                             category_col='decision',
                             text_col='text_clean',
                             nlp=nlp).build().remove_terms(Mystopwords, ignore_absences=True)

html3 = st.produce_scattertext_explorer(keepXraise,
                                       category=keep,
                                       category_name=keep,
                                       not_category_name=raise_,
                                       width_in_pixels=1000,
                                       )
open("keep_x_raise.html", 'wb').write(html3.encode('utf-8'))