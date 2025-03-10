import textstat
import numpy as np
import matplotlib.pyplot as plt
from load_texts import read_text_files, return_data_frame

print("Loading data...")
corpus = read_text_files()[0]
print(len(corpus), "minutes")

atas = np.arange(21, 21+len(corpus), 1)
# Calculate indexes
ari = np.zeros(atas.shape)
cli = np.zeros(atas.shape)
fre = np.zeros(atas.shape)
for i in range(len(corpus)):
    #Automated Readability Index 
    ari[i] = textstat.automated_readability_index(corpus[i])
    #Coleman Liau Index
    cli[i] = textstat.coleman_liau_index(corpus[i])
    #Flesch Reading Ease
    fre[i] = textstat.flesch_reading_ease(corpus[i])


#Automated Readability Index 
plt.plot(atas, ari)
plt.xlabel('Atas')
plt.ylabel('ARI')
plt.title('textstat - Automated Readability Index')
plt.show()

#Coleman Liau Index
plt.plot(atas, cli)
plt.xlabel('Atas')
plt.ylabel('CLI')
plt.title('textstat - Coleman Liau Index')
plt.show()

#Flesch Reading Ease
plt.plot(atas, fre)
plt.xlabel('Atas')
plt.ylabel('FRE')
plt.title('textstat - Flesch Reading Ease')
plt.show()


##-----------------------------------------------------------------------------
# Indexes adapted to Portuguese 
# https://legibilidade.com/sobre
# https://arxiv.org/pdf/2203.12135

print("Portuguese metrics ...")

import re
from hyphen import Hyphenator # pip install PyHyphen
from nltk.tokenize import RegexpTokenizer, sent_tokenize

def words(text):
    tok = RegexpTokenizer(r'\w+')
    return tok.tokenize(text)

def NrWords(text):
    listWords = words(text)
    return len(listWords)

def NrComplexWords(text):
    listWords = words(text)
    listWordSyllables = [syllables(word) for word in listWords]
    count = 0
    for wordSyllables in listWordSyllables:
        if len(wordSyllables) > 2:
            count += 1
    return count

def NrSentences(text):
    sentences = sent_tokenize(text)
    return len(sentences)

def NrLetters(text):
    text = re.sub('[a-zA-Z]','', text)
    return len(text)

def syllables(text):
    words_ = words(text)
    model=Hyphenator('pt_BR')
    listSyllables = []
    for w in words_:
        listSyllables += model.syllables(w)
    return listSyllables

def NrSyllables(text):
    listSyllables = syllables(text)
    return len(listSyllables)

    

def fleschReadingEase(text):
    nrword = NrWords(text)
    return 226 - 1.04 * (nrword / NrSentences(text)) - 72 * (NrSyllables(text) / nrword)

def gulpeaseIndex(text):
    return 89 + (300 * NrSentences(text) - 10 * NrLetters(text)) / NrWords(text)

def fleschKincaid(text):
    nrword = NrWords(text)
    return 0.36 * (nrword / NrSentences(text)) + 10.4 * (NrSyllables(text) / nrword) -18

def gunningFox(text):
    nrword = NrWords(text)
    return 0.49 * (nrword / NrSentences(text)) + 19 * (NrComplexWords(text) / nrword)

def automatedReadabilityIndex(text):
    nrword = NrWords(text)
    return 4.6 * (NrLetters(text) / nrword) + 0.44 * (nrword / NrSentences(text))

def colemanLiauIndex(text):
    nrword = NrWords(text)
    return 5.4 * (NrLetters(text) / nrword) - 21 * (NrSentences(text) / nrword) - 14

# Extra function
def timeReading(text, wordsPerMinute = 200):
    return NrWords(text) / wordsPerMinute
    

df = return_data_frame()
df=df.tail(60)
df["fleschReadingEase"] = df["text"].apply(fleschReadingEase)
df["fleschReadingEase"].plot(title = "fleschReadingEase")
plt.show()
df["gulpeaseIndex"] = df["text"].apply(gulpeaseIndex)
df["gulpeaseIndex"].plot(title="gulpeaseIndex")
plt.show()
df["fleschKincaid"] = df["text"].apply(fleschKincaid)
df["fleschKincaid"].plot(title = "fleschKincaid")
plt.show()
df["gunningFox"] = df["text"].apply(gunningFox)
df["gunningFox"].plot(title = "gunningFox")
plt.show()
df["automatedReadabilityIndex"] = df["text"].apply(automatedReadabilityIndex)
df["automatedReadabilityIndex"].plot(title = "automatedReadabilityIndex")
plt.show()
df["colemanLiauIndex"] = df["text"].apply(colemanLiauIndex)
df["colemanLiauIndex"].plot(title = "colemanLiauIndex")
plt.show()
df["timeReading"] = df["text"].apply(timeReading)
df["timeReading"].plot(title = "timeReading")
plt.show()