import textstat
import numpy as np
import matplotlib.pyplot as plt
from load_texts import read_text_files, Mystopwords

print("Loading data...")
corpus = read_text_files()[0]
print(len(corpus), "minutes")

#Automated Readability Index 
atas = np.arange(20, 20+len(corpus), 1)
ari = np.zeros(atas.shape)
for i in range(len(corpus)):
    ari[i] = textstat.automated_readability_index(corpus[i])

plt.plot(atas, ari)
plt.xlabel('Atas')
plt.ylabel('ARI')
plt.title('Automated Readability Index')
plt.show()
