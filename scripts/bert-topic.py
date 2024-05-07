from bertopic import BERTopic
from load_texts import *

print('loading texts...')
df = return_data_frame()
# print(df.info())

print('removing stop words...')
Mystopwords = Mystopwords + ['aa','anterior','ao','banco','carlos','central','comitê','conforme','copom','dia','dias','dos','doze',
                             'edições','entanto','hoje','item','luiz','membros','mensal','meses','mil','monetária','número','os','otávio','pb','período',
                             'política','pp','quarto','realizou','relação','repectivamente','reunião','se','três','últimas',
                             'trimestre','trimestres','variou','']
corpus = df['text'].to_list()

PARAGRAPHS = True

if PARAGRAPHS:
    corpusJoined = '\n'.join(corpus)
    corpusJoined = re.sub('\n \n', '\n', corpusJoined) 
    corpus_aux = corpusJoined.split('\n')
    corpus = []
    for txt in corpus_aux:
        if (txt != '') & (txt != ' '):
            corpus.append(txt)
    print(len(corpus), "paragraphs")
    ngram_range = (1, 1)
    minTopicSize = 100
else:
    ngram_range = (2, 3)
    minTopicSize = 10

for i in range(0, len(corpus)):
    words = corpus[i].split(" ")
    words_new = [w for w in words if w not in Mystopwords]
    corpus[i] = ' '.join(words_new)

del words, words_new

print('running bertopic...')
topic_model = BERTopic(language='multilingual',
                                verbose=True,
                                calculate_probabilities=True,
                                n_gram_range=ngram_range,
                                min_topic_size=minTopicSize)
topics, probs = topic_model.fit_transform(corpus)

topic_info = topic_model.get_topic_info()
print(topic_info[["Topic","Count","Representation"]])

for i in range(len(topic_model.get_topics())):
    if i < topic_info.shape[0]-1:
        print('Topic %.0f' % i)
        print([n for n, p in topic_model.get_topic(i)])
        # print(topic_model.get_representative_docs(topic=i))
    print()

doc_info = topic_model.get_document_info(corpus)

print(doc_info[["Document","Topic","Probability","Top_n_words"]])

topic_model.visualize_barchart(top_n_topics=12, n_words=10, height=500)

for i in range(0, len(corpus)):
    words = corpus[i].split(" ")
    if len(words) == 0:
        print(i)

