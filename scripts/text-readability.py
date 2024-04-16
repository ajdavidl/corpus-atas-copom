import textstat
import numpy as np
import matplotlib.pyplot as plt
from load_texts import read_text_files, Mystopwords

print("Loading data...")
corpus = read_text_files()[0]
print(len(corpus), "minutes")

atas = np.arange(20, 20+len(corpus), 1)
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
plt.title('Automated Readability Index')
plt.show()

#Coleman Liau Index
plt.plot(atas, cli)
plt.xlabel('Atas')
plt.ylabel('CLI')
plt.title('Coleman Liau Index')
plt.show()

#Flesch Reading Ease
plt.plot(atas, fre)
plt.xlabel('Atas')
plt.ylabel('FRE')
plt.title('Flesch Reading Ease')
plt.show()