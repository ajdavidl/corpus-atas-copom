from bertopic import BERTopic
from load_texts import *

print('loading texts...')
df = return_data_frame()
# print(df.info())

print('removing stop words...')
corpus = df['text'].to_list()

for i in range(0, len(corpus)):
    words = corpus[i].split(" ")
    words_new = [w for w in words if w not in Mystopwords]
    corpus[i] = ' '.join(words_new)
df['text_clean'] = corpus

del words, words_new

print('running bertopic...')
topic_model = BERTopic(language='multilingual',
                                verbose=True,
                                calculate_probabilities=True,
                                n_gram_range=(2, 3),
                                min_topic_size=10)
topics, probs = topic_model.fit_transform(corpus)

print(topic_model.get_topic_info())

print(topic_model.get_topics())

for i in range(len(topic_model.get_topics())):
    print('Topic %.0f' % i)
    print([n for n, p in topic_model.get_topic(i)])
    # print(topic_model.get_representative_docs(topic=i))
    print()

print(topic_model.get_document_info(corpus))
