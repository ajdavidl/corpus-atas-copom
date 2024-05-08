from multi_rake import Rake
from load_texts import read_text_files, Mystopwords

Mystopwords = Mystopwords + ["além", "algum", "alguma", "algumas", "alguns", "anterior", "banco", "bancos", "centrais", "central", "copom", "disso", "doze", "focus" "índice", "inflação", "meta", "monetária", "período", "pesquisa", "política", 
    "preço", "preços", "relação", "reunião", "taxa", "última"] + ["um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"]

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