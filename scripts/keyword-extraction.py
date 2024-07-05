import re
from multi_rake import Rake
from load_texts import *


def limpa_string(line):
    """Faz a limpeza da string removendo caracteres indesejados"""
    line = re.sub('[0-9]+', '', line) #numbers
    line = re.sub('º','',line)
    line = re.sub('ª','',line)
    line = re.sub('%','',line)
    line = re.sub('@','',line)
    line = re.sub('=',' ',line)
    line = re.sub('#','',line)
    line = re.sub('\*','',line)
    line = re.sub('_',' ',line)
    line = re.sub('\|',' ',line)
    line = re.sub('«','',line)
    line = re.sub('»','',line)
    return line

Mystopwords = Mystopwords + ["além", "algum", "alguma", "algumas", "alguns", "anexo", "anterior", "banco", "bancos", "bond", "bonds", "centrais", "central", "copom", "disso", "federal", "finanças", "focus" "índice", 
"inflação", "meta", "monetária", "período", "pesquisa", "política", 
    "preço", "preços", "públicas", "quadrissemana", "reserve", "s/a" "relação", "reunião", "taxa", "última"] + ["um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze", "1ª"]

def print_keywords(key_list):
    """
    key_list : list of tuples
    """
    count = 1
    for tup in key_list:
        print(count,")", sep='', end=' ')
        for word in tup:
            print(word, end=' ')
        print()
        count+=1

print("Loading data...")
corpus = read_text_files()[0]
print(len(corpus), "minutes")

atas = [i for i in range(21, 21+len(corpus))]

rake = Rake(min_chars=4,
            max_words=2,
            min_freq=1,
            stopwords = Mystopwords)

nr_docs = 10

for i in range(len(corpus)-nr_docs, len(corpus)):
    print("Minute:", atas[i])
    keywords = rake.apply( corpus[i].lower() )
    print(keywords[:10])

# Keywords for each decision
print("\nKeywords for each decision!")
start_index = 150
print("Starting in the meeting:", start_index+21)
df_total = return_data_frame()

df = df_total[df_total["meeting"] > 150]
df['text_clean'] = df['text'].apply(limpa_string)

list_keep = df[df['decision'] == 'keep']['text_clean'].to_list()
list_raise = df[df['decision'] == 'raise']['text_clean'].to_list()
list_lower = df[df['decision'] == 'lower']['text_clean'].to_list()

print()
number_keywords = 20
print("Raise:")
print(len(list_raise),"atas")
keys_raise = rake.apply( '\n'.join(list_raise).lower() )
print_keywords(keys_raise[:number_keywords])
print()
print("Lower:")
print(len(list_lower),"atas")
keys_lower = rake.apply( '\n'.join(list_lower).lower() )
print_keywords(keys_lower[:number_keywords])
print()
print("Keep:")
print(len(list_keep),"atas")
keys_keep = rake.apply( '\n'.join(list_keep).lower() )
print_keywords(keys_keep[:number_keywords])
