import re
import wordcloud
import matplotlib.pyplot as plt
from load_texts import *  # return_data_frame() and Mystopwords

Mystopwords = Mystopwords + ["anterior", "banco", "central", "copom", "doze", "índice", "inflação", "meta", "monetária", "período", "política", 
    "preço", "preços", "relação", "taxa"]

def wordcloudPlot(text, stopwords=None, title = "", max_font_size=50, max_words=100, background_color="white"):
    cloud = wordcloud.WordCloud(stopwords=stopwords, max_font_size=max_font_size,
                                max_words=max_words, background_color=background_color).generate(text.lower())

    # Display the generated image:
    plt.imshow(cloud, interpolation='bilinear')
    plt.title(title)
    plt.axis("off")
    plt.show()


print("Loading data...")
dfCorpus = return_data_frame()
dfCorpus.text = dfCorpus.text.apply(lambda x : x.lower())
corpus = dfCorpus.text.to_list()
print(len(corpus), "minutes")

corpusLower = dfCorpus[dfCorpus.decision == "lower"].text.to_list()
print(len(corpusLower), "minutes - lower")
corpusRaise = dfCorpus[dfCorpus.decision == "raise"].text.to_list()
print(len(corpusRaise), "minutes - raise")
corpusKeep = dfCorpus[dfCorpus.decision == "keep"].text.to_list()
print(len(corpusKeep), "minutes - keep")

corpusJoined = ' '.join(corpus)
corpusJoined = corpusJoined.lower()
corpusJoined = re.sub('\n', '', corpusJoined)  

corpusLowerJoined = ' '.join(corpusLower)
corpusLowerJoined = corpusLowerJoined.lower()
corpusLowerJoined = re.sub('\n', '', corpusLowerJoined)  

corpusRaiseJoined = ' '.join(corpusRaise)
corpusRaiseJoined = corpusRaiseJoined.lower()
corpusRaiseJoined = re.sub('\n', '', corpusRaiseJoined)  

corpusKeepJoined = ' '.join(corpusKeep)
corpusKeepJoined = corpusKeepJoined.lower()
corpusKeepJoined = re.sub('\n', '', corpusKeepJoined)  

wordcloudPlot(corpusJoined, stopwords=Mystopwords, title="Minutes")
wordcloudPlot(corpusLowerJoined, stopwords=Mystopwords, title="Lower")
wordcloudPlot(corpusRaiseJoined, stopwords=Mystopwords, title="Raise")
wordcloudPlot(corpusKeepJoined, stopwords=Mystopwords, title="Keep")
