import matplotlib.pyplot as plt
from transformers import pipeline, AutoTokenizer
from load_texts import *

model = "lucas-leme/FinBERT-PT-BR"
pipe = pipeline("text-classification", model=model, return_all_scores = True, device=0)
tokenizer = AutoTokenizer.from_pretrained(model)

print("Loading data...")
dfCorpus = return_data_frame()
corpus = dfCorpus.text.to_list()
print(len(corpus), "atas")

size = 1750 #characters
corpus_trunc = [txt[:size] for txt in corpus]

out = pipe(corpus_trunc)

positive_scores = []
neutral_scores = []
negative_scores = []

# Get sentiment scores
for l in out:
    for d in l:
        if d['label'] == 'POSITIVE':
            positive_scores.append(d['score'])
        elif d['label'] == 'NEUTRAL':
            neutral_scores.append(d['score'])
        elif d['label'] == 'NEGATIVE':
            negative_scores.append(d['score'])
        else:
            raise('Error in label', d)

dfCorpus['positive_scores'] = positive_scores
dfCorpus['neutral_scores'] = neutral_scores
dfCorpus['negative_scores'] = negative_scores

def df_plot(column):
    plt.figure()
    dfCorpus[column].plot()
    plt.title(column)
    plt.ylabel("score")
    plt.xlabel("meeting")
    plt.show()

df_plot('positive_scores')
df_plot('neutral_scores')
df_plot('negative_scores')