import nltk
import os

print("Loading data...")
AtasFolder = "../atas"
listAtas = os.listdir(AtasFolder)

corpus = []
for ata in listAtas:
    with open(AtasFolder + "/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines).lower()
            corpus.append(lines)

print(len(corpus), "minutes")


def concordance(listSentences, word):
    tokens = nltk.word_tokenize("\n".join(listSentences))
    text1 = nltk.Text(tokens)
    results = text1.concordance_list(word, width=100, lines=20)
    textOutput = ""
    for i in range(len(results)):
        textOutput = textOutput + \
            results[i][4] + " " + results[i][1] + " " + results[i][5] + "\n"
    return(textOutput)


print(concordance(corpus, "inflação"))
print(concordance(corpus, "ipca"))
print(concordance(corpus, "juros"))
print(concordance(corpus, "selic"))
print(concordance(corpus, "câmbio"))
print(concordance(corpus, "dólar"))
print(concordance(corpus, "atividade"))
print(concordance(corpus, "pib"))
