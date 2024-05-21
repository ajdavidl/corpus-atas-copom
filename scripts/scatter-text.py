import re
import spacy
import scattertext as st
from load_texts import *  

nlp = spacy.load('pt_core_news_sm')


def removeNumbers(string):
    if type(string)!=str:
        return(string)
    string = re.sub('[0-9]+','',string)
    return(string)

print('loading texts...')
df = return_data_frame()
print(df.shape[0], "minutes")

Mystopwords = Mystopwords + ["banco","central","copom","doze","membros","meses","os","se"]
corpus = df['text'].to_list()

for i in range(len(corpus)):
    corpus[i] = removeNumbers(corpus[i])
df['text_clean'] = corpus

print("Doing lower X raise")
lowerXraise = st.CorpusFromPandas(df[df['decision'].isin(['lower','raise'])],
                             category_col='decision',
                             text_col='text_clean',
                             nlp=nlp).build().remove_terms(Mystopwords, ignore_absences=True)

html = st.produce_scattertext_explorer(lowerXraise,
                                       category='lower',
                                       category_name='lower',
                                       not_category_name='raise',
                                       width_in_pixels=1000,
                                       )
open("raise_x_lower.html", 'wb').write(html.encode('utf-8'))

print("Doing lower X keep")
lowerXkeep = st.CorpusFromPandas(df[df['decision'].isin(['lower','keep'])],
                             category_col='decision',
                             text_col='text_clean',
                             nlp=nlp).build().remove_terms(Mystopwords, ignore_absences=True)

html2 = st.produce_scattertext_explorer(lowerXkeep,
                                       category='lower',
                                       category_name='lower',
                                       not_category_name='raise',
                                       width_in_pixels=1000,
                                       )
open("keep_x_lower.html", 'wb').write(html2.encode('utf-8'))

print("Doing raise X keep")
keepXraise = st.CorpusFromPandas(df[df['decision'].isin(['raise','keep'])],
                             category_col='decision',
                             text_col='text_clean',
                             nlp=nlp).build().remove_terms(Mystopwords, ignore_absences=True)

html3 = st.produce_scattertext_explorer(keepXraise,
                                       category='keep',
                                       category_name='keep',
                                       not_category_name='raise',
                                       width_in_pixels=1000,
                                       )
open("keep_x_raise.html", 'wb').write(html3.encode('utf-8'))