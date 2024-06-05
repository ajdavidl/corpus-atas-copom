import re
import nltk
import numpy as np
import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt
from load_texts import *  # return_data_frame() and Mystopwords

# MODELOS

nlp = spacy.load('pt_core_news_sm')

# LISTAS

list_pronoums = ["eu","tu","você","ele","ela","nós","vós","vocês","eles",
                     "elas","me","mim","comigo","te","ti","contigo","lhe","si",
                     "nos","conosco","vos","convosco","lhes","vossa senhoria",
                     "meu","minha","meus","minhas","teu","tua","teus","tuas",
                     "seu","sua","seus","suas","nosso","nossa","nossos","nossas",
                     "vosso","vossa","vossos","vossas","este","esta","estes",
                     "estas","isto","neste","nesta","nestes","nestas","nisto",
                     "deste","desta","destes","destas","disto","esse","essa",
                     "esses","essas","isso","nesse","nessa","nesses","nessas",
                     "nisso","desse","dessa","desses","dessas","disso","aquele",
                     "aquela","aqueles","aquelas","aquilo","naquele","naquela",
                     "naqueles","naquelas","naquilo","daquele","daquela",
                     "daquele","daquelas","daquilo","àquele","àquela","àqueles",
                     "àquelas","àquilo","qual","quais","quanto","quantos","quanta",
                     "quantas","quem","que","algum","alguma","alguns","algumas",
                     "nenhum","nenhuma","nenhuns","nenhumas","muito","muita",
                     "muitos","muitas","pouco","pouca","poucos","poucas","todo",
                     "toda","todos","todas","tanto","tanta","tantos","tantas",
                     "qualquer","quaisquer","alguém","ninguém","tudo","nada",
                     "outrem","algo","cada","a gente"] #senhor","senhora #o,a,os,as,se,que
list_pronoums2 = ["eu","tu","você","vocês","a gente"]
list_conjunctions_fund_1 = [ "como", "se", "mas", "quando", "ou", "que", 
                                "porque", "e", "assim", "porém", "caso", 
                                "por isso que", "por isso", "por enquanto", 
                                "enquanto isso", "enquanto", "pois", "além de", 
                                "então", "daí", "por exemplo", "ou seja", 
                                "sem que", "para que", "cada vez que", 
                                "antes que", "assim como", "tanto quanto", 
                                "que nem", "toda vez que", "a não ser que", 
                                "depois que", "até que", "na medida em que", "desde", 
                                "nem bem", "tanto que", "segundo", "assim que", 
                                "tanto que", "tão que", "sem que", "ora"] #"feito", 
list_conjunctions_fund_2 = ["todavia", "eis", "a fim de", "ao passo que", "para que", 
                                "conforme", "tais", "ou seja", "contudo", "bem como", "logo", 
                                "à medida que", "entretanto", "desde que", "mesmo que", 
                                "ainda que", "de acordo com", "uma vez que", "por sua vez", 
                                "sobretudo", "até", "ainda", "caso", "no entanto", 
                                "nem", "quanto", "já", "como", "já que", "outrossim", 
                                "mas também", "como também", "não só", "mas ainda", 
                                "tampouco", "senão também", "bem assim", "ademais", "antes", 
                                "não obstante", "sem embargo", "ao passo que", 
                                "de outra forma", "em todo caso", "aliás", "de outro modo", 
                                "por conseguinte", "em consequência de", "por consequência", 
                                "consequentemente", "conseguintemente", "isso posto", "pelo que", 
                                "de modo que", "de maneira que", "de forma que", "em vista disso", 
                                "por onde", "porquanto", "posto que", "isto é", "ademais", 
                                "senão", "dado que", "visto como", "vez que", "de vez que", 
                                "pois que", "agora", "na medida em que", "sendo que", "como que", 
                                "como quer que", "eis que", "sendo assim", "tal qual", 
                                "ao invés de", "conquanto", "por muito que", "visto que", 
                                "uma vez que", "quanto mais", "quanto menos", "se bem que", 
                                "apesar de que", "suposto que", "ainda quando", "quando mesmo", 
                                "a despeito de", "conquanto que", "sem embargo de que", 
                                "por outro lado", "em contrapartida", "sem embargo", "muito embora", 
                                "inclusive se", "por mais que", "por menos que", "por pouco que", 
                                "contanto que", "salvo se", "com tal que", "caso que", "consoante", 
                                "tal que", "de forma que", "à proporção que", "ao passo que", 
                                "mal", "tão logo", "entretanto", "sob esse aspecto", "sob esse prisma", 
                                "sob esse ponto de vista", "sob esse enfoque", "embora", "portanto", 
                                "além disso"]
list_indefinite_pronouns = ["nada", "ninguém", "alguém", "qualquer","tudo","algum","alguma","alguns","algumas","nenhum","nenhuma","nenhuns","nenhumas","todo","toda","todos","todas","tanto","tanta","tantos","tantas",
"qualquer","quaisquer","alguém","ninguém","tudo","nada","outrem","algo","cada","cada um", "cada qual", "qualquer um", "seja qual for", "seja quem for", "todo aquele que"]
lista_conectivos_aditivos_negativos = ['mas','porém','contudo','todavia','no entanto','se não','não obstante','ainda assim','apesar disso','mesmo assim','de outra sorte','ao passo que','entretanto']
lista_conectivos_aditivos = ['e','nem','também','bem como','como também','ainda','mais','e não','não só', 'mas também','tanto quanto','além de', 'além disto', 'além daquilo', 'além disso']#, 'em vez de']
lista_conectivos_causais_negativos = ['mesmo embora', 'contudo', 'no entanto', 'apesar de', 'apesar disso', 'apesar disto', 'a menos que']
lista_conectivos_causais_positivos = ['habilita', 'para', 'se', 'somente se', 'assim', 'porque', 
                                      'pois', 'porquanto', 'pois que', 'por isso que', 'uma vez que',
                                      'visto que', 'visto como']#, 'para isso', 'que']
lista_conectivos_logicos_negativos = ['pelo contrário', 'ainda', 'cada vez que','embora']
lista_conectivos_logicos_positivos = ['similarmente', 'por outro lado', 'de novo', 'somente se', 'assim', 'para este fim']
lista_operadores_logicos = [' ou ', ' e ', ' se ', 'não']
lista_palavras_negacao = ['não', 'nem', 'nunca', 'tampouco', 'jamais']
lista_conectivos_temporais_positivos = ['assim', 'outra vez', 'imediatamente','enquanto', 'finalmente']

def NILCMetrix(txt):
    """
    Calcula uma amostra das métricas do NILC-Metrix
    http://fw.nilc.icmc.usp.br:23380/metrixdoc
    Recebe uma string e devolve um dicionário python com as métricas
    """
    metricas = {}
    
    txt_sent_tokenized = nltk.sent_tokenize(txt.lower())
    text = []
    pos = []
    tag = []
    dep = []
    ent_text = []
    ent_label = []
    list_df_sent_parse = []
    for sentence in txt_sent_tokenized:
        sent_text = []
        sent_pos = []
        sent_tag = []
        sent_dep = []
        sent_id = []
        doc = nlp(sentence)
        for token in doc:
            text.append(token.text)
            pos.append(token.pos_)
            tag.append(str(token.morph))
            dep.append(token.dep_)
            sent_text.append(token.text)
            sent_pos.append(token.pos_)
            sent_tag.append(str(token.morph))
            sent_dep.append(token.dep_)
            sent_id.append(token.i)
        for ent in doc.ents:
            ent_text.append(ent.text)
            ent_label.append(ent.label_)
        df_aux = pd.DataFrame(list(zip(sent_text, sent_pos, sent_tag, sent_dep, sent_id)), 
                   columns =['word', 'pos','tag','dep','id'])
        list_df_sent_parse.append(df_aux)
    del df_aux, sent_pos, sent_text, sent_tag, sent_dep, sent_id
    df = pd.DataFrame(list(zip(text, pos, tag, dep)), 
               columns =['word', 'pos', 'tag', 'dep'])
    
    
    # 1. MEDIDAS DESCRITIVAS
    
    # Quantidade de Parágrafos no texto (id: 152)
    paragraphs = len(nltk.tokenize.line_tokenize(txt))
    metricas['paragraphs'] = paragraphs
    
    # Quantidade de Sentenças no texto (id: 154)
    sentences = len(txt_sent_tokenized)
    metricas['sentences'] = sentences
    
    # Quantidade média de sentenças por parágrafo no texto (id: 155)
    sentences_per_paragraph = sentences/paragraphs 
    metricas['sentences_per_paragraph'] = sentences_per_paragraph
    
    # Quantidade média de sílabas por palavra no texto (id: 157)
    # syllables_per_content_word
    
    # Quantidade de Palavras no texto (id: 158)
    txt_word_tokenized = nltk.word_tokenize(txt)
    words = len(txt_word_tokenized)
    metricas['words'] = words
    
    # Média de Palavras por Sentença (id: 159)
    words_per_sentence = words/sentences
    metricas['words_per_sentence'] = words_per_sentence
    
    # Quantidade Máxima de palavras por sentença (id: 153)
    txt_sent_word_tokenized = [nltk.word_tokenize(s) for s in txt_sent_tokenized]
    nr_word_per_sentence = [len(l) for l in txt_sent_word_tokenized]
    sentence_length_max = max(nr_word_per_sentence)
    metricas['sentence_length_max'] = sentence_length_max
    
    # Quantidade Mínima de palavras por sentença (id: 184)
    sentence_length_min = min(nr_word_per_sentence)
    metricas['sentence_length_min'] = sentence_length_min
    
    # Desvio Padrão da quantidade de palavras por sentença (id: 185)
    sentence_length_standard_deviation = np.std(nr_word_per_sentence)
    metricas['sentence_length_standard_deviation'] = sentence_length_standard_deviation
    
    # Proporção de subtítulos em relação à quantidade de sentenças do texto (id: 156)
    # subtitles
    
    # 2. SIMPLICIDADE TEXTUAL
        
    # Proporção de pronomes pessoais que indicam uma conversa com o leitor em relação à quantidade de pronomes pessoais do texto (id: 186)
    nr_pron = 0
    nr_pron2 = 0
    for w in list_pronoums:
        nr_pron += txt.count(w)
    for w in list_pronoums2:
        nr_pron2 += txt.count(w)
    dialog_pronoun_ratio = nr_pron2/nr_pron
    metricas['dialog_pronoun_ratio'] = dialog_pronoun_ratio
    
    # Proporção de conjunções fáceis em relação à quantidade de palavras do texto (id: 187)
    nr_conj_easy = 0
    for w in list_conjunctions_fund_1:
        nr_conj_easy += txt.count(w)
    easy_conjunctions_ratio = nr_conj_easy/words
    metricas['easy_conjunctions_ratio'] = easy_conjunctions_ratio
    
    # Proporção de conjunções difíceis em relação à quantidade de palavras do texto (id: 188)
    nr_conj_hard = 0
    for w in list_conjunctions_fund_2:
        nr_conj_hard += txt.count(w)
    hard_conjunctions_ratio = nr_conj_hard/words
    metricas['hard_conjunctions_ratio'] = hard_conjunctions_ratio
    
    # Proporção de Sentenças Muito Longas em relação a todas as sentenças do texto (id: 189)
    long_sentence_ratio = len([n for n in nr_word_per_sentence if n > 15])  / sentences
    metricas['long_sentence_ratio'] = long_sentence_ratio
    
    # Proporção de Sentenças Longas em relação a todas as sentenças do texto (id: 190)
    medium_long_sentence_ratio = len([n for n in nr_word_per_sentence if (n==14) or (n == 15)])  / sentences
    metricas['medium_long_sentence_ratio'] = medium_long_sentence_ratio
    
    # Proporção de Sentenças Médias em relação a todas as sentenças do texto (id: 191)
    medium_short_sentence_ratio = len([n for n in nr_word_per_sentence if (n==12) or (n == 13)])  / sentences
    metricas['medium_short_sentence_ratio'] = medium_short_sentence_ratio
    
    # Proporção de Sentenças Curtas em relação a todas as sentenças do texto (id: 192)
    short_sentence_ratio = len([n for n in nr_word_per_sentence if n <= 11 ])  / sentences
    metricas['short_sentence_ratio'] = short_sentence_ratio
    
    # Proporção de palavras de conteúdo simples em relação a todas palavras de conteúdo do texto (id: 193)
    # simple_word_ratio
    
    # 3. COESÃO REFERENCIAL
    
    # Média das proporções de candidatos a referentes na sentença anterior em relação aos pronomes pessoais do caso reto nas sentenças (id: 17)
    # adjacent_refs
    
    # Média das proporções de candidatos a referentes nas 5 sentenças anteriores em relação aos pronomes anafóricos das sentenças (id: 18)
    # anaphoric_refs
    
    # Quantidade média de referentes que se repetem nos pares de sentenças adjacentes do texto (id: 1)
    # adj_arg_ovl
    
    # Quantidade média de palavras de conteúdo que se repetem nos pares de sentenças adjacentes do texto (id: 2)
    # adj_cw_ovl
    
    # Quantidade média de radicais de palavras de conteúdo que se repetem nos pares de sentenças adjacentes do texto. (id: 3)
    # adj_stem_ovl
    
    # Quantidade média de referentes que se repetem nos pares de sentenças do texto (id: 4)
    # arg_ovl
    
    # Quantidade média de radicais de palavras de conteúdo que se repetem nos pares de sentenças do texto (id: 5)
    # stem_ovl
    
    # Média de candidatos a referente, na sentença anterior, por pronome anafórico do caso reto (id: 194)
    # coreference_pronoun_ratio
    
    # Média de candidatos a referente, na sentença anterior, por pronome demonstrativo anafórico (id 195)
    # demonstrative_pronoun_ratio
    
    # 4. COESÃO SEMÂNTICA
    
    # Média de similaridade entre pares de sentenças adjacentes no texto (id: 7)
    # lsa_adj_mean
    
    # Desvio padrão de similaridade entre pares de sentenças adjacentes no texto (id: 8)
    # lsa_adj_std
    
    # Média de similaridade entre todos os pares de sentenças no texto (id: 9)
    # lsa_all_mean
    
    # Desvio padrão de similaridade entre todos os pares possíveis de sentenças do texto (id: 10)
    # lsa_all_std
    
    # Média do *givenness* da cada sentença do texto, a partir da segunda (id: 11)
    # lsa_givenness_mean
    
    # Desvio padrão do *givenness* da cada sentença do texto, a partir da segunda (id: 12)
    # lsa_givenness_std
    
    # Média de similaridade entre pares de parágrafos adjacentes no texto (id: 13)
    # lsa_paragraph_mean
    
    # Desvio padrão entre parágrafos adjacentes no texto (id: 14)
    # lsa_paragraph_std
    
    # Média do *span* da cada sentença do texto, a partir da segunda (id: 15)
    # lsa_span_mean
    
    # Desvio padrão do span da cada sentença do texto, a partir da segunda (id: 16)
    # lsa_span_std
    
    # Média da entropia cruzadas das sentenças do texto (id: 6)
    # cross_entropy
    
    # 5. MEDIDAS PSICOLINGUÍSTICAS
    
    # Proporção de palavras com valor de concretude entre 1 e 2,5 em relação a todas as palavras de conteúdo do texto (id: 160)
    # concretude_1_25_ratio
    
    # Proporção de palavras com valor de concretude entre 2,5 e 4 em relação a todas as palavras de conteúdo do texto (id: 161)
    # concretude_25_4_ratio
    
    # Proporção de palavras com valor de concretude entre 4 e 5,5 em relação a todas as palavras de conteúdo do texto (id: 162)
    # concretude_4_55_ratio
    
    # Proporção de palavras com valor de concretude entre 5,5 e 7 em relação a todas as palavras de conteúdo do texto (id 163)
    # concretude_55_7_ratio
    
    # Média dos valores de concretude das palavras de conteúdo do texto (id: 164)
    # concretude_mean
    
    # Desvio padrão do valor de concretude das palavras de conteúdo do texto (id: 165)
    # concretude_std
    
    # Proporção de palavras com valor de familiaridade entre 1 e 2,5 em relação a todas as palavras de conteúdo do texto (id: 166)
    # familiaridade_1_25_ratio
    
    # Proporção de palavras com valor de familiaridade entre 2,5 e 4 em relação a todas as palavras de conteúdo do texto (id: 167)
    # familiaridade_25_4_ratio
    
    # Proporção de palavras com valor de familiaridade entre 4 e 5,5 em relação a todas as palavras de conteúdo do texto (id: 168)
    # familiaridade_4_55_ratio
    
    # Proporção de palavras com valor de familiaridade entre 5,5 e 7 em relação a todas as palavras de conteúdo do texto (id: 169)
    # familiaridade_55_7_ratio
    
    # Média dos valores de familiaridade das palavras de conteúdo do texto (id: 170)
    # familiaridade_mean
    
    # Desvio padrão dos valores de familiaridade das palavras de conteúdo do texto (id: 171)
    # familiaridade_std
    
    # Proporção de palavras com valor de idade de aquisição entre 1 e 2,5 em relação a todas as palavras de conteúdo do texto (id: 172)
    # idade_aquisicao_1_25_ratio
    
    # Proporção de palavras com valor de idade de aquisição entre 2,5 e 4 em relação a todas as palavras de conteúdo do texto (id: 173)
    # idade_aquisicao_25_4_ratio
    
    # Proporção de palavras com valor de idade de aquisição entre 4 e 5,5 em relação a todas as palavras de conteúdo do texto (id: 174)
    # idade_aquisicao_4_55_ratio
    
    # Proporção de palavras com valor de idade de aquisição entre 5,5 e 7 em relação a todas as palavras de conteúdo do texto (id: 175)
    # idade_aquisicao_55_7_ratio
    
    # Média dos valores de idade de aquisição das palavras de conteúdo do texto (id: 176)
    # idade_aquisicao_mean
    
    # Desvio padrão dos valores de idade de aquisição das palavras de conteúdo do texto (id: 177)
    # idade_aquisicao_std
    
    # Proporção de palavras com valor de imageabilidade entre 1 e 2,5 em relação a todas as palavras de conteúdo do texto (id: 178)
    # imageabilidade_1_25_ratio
    
    # Proporção de palavras com valor de imageabilidade entre 2,5 e 4 em relação a todas as palavras de conteúdo do texto (id: 179)
    # imageabilidade_25_4_ratio
    
    # Proporção de palavras com valor de imageabilidade entre 4 e 5,5 em relação a todas as palavras de conteúdo do texto (id: 180)
    # imageabilidade_4_55_ratio
    
    # Proporção de palavras com valor de imageabilidade entre 5,5 e 7 em relação a todas as palavras de conteúdo do texto (id: 181)
    # imageabilidade_55_7_ratio
    
    # Média dos valores de imageabilidade das palavras de conteúdo do texto (id: 182)
    # imageabilidade_mean
    
    # Desvio padrão dos valores de imageabilidade das palavras de conteúdo do texto (id: 183)
    # imageabilidade_std
    
    # 6. DIVERSIDADE LEXICAL 
    
    # Proporção de types (despreza repetições de palavras) em relação à quantidade de tokens (computa repetições de palavras) no texto (id: 75)
    word_freq = Counter(txt_word_tokenized)
    ttr = len(word_freq)/words
    metricas['ttr'] = ttr
    
    # Proporção de types de adjetivos em relação à quantidade de tokens de adjetivos no texto (id: 62)
    df_aux = df[df['pos'] == 'ADJ']
    adjective_diversity_ratio = df_aux.word.unique().shape[0] / df_aux.shape[0]
    del df_aux
    metricas['adjective_diversity_ratio'] = adjective_diversity_ratio
    
    # Proporção de palavras de conteúdo em relação à quantidade de palavras funcionais do texto (id: 63)
    #palavras de conteudo
    df_aux = df[ (df['pos'] == 'PROPN') | (df['pos'] == 'NOUN') | (df['pos'] == 'ADJ') | (df['pos'] == 'AUX') | (df['pos'] == 'VERB') | (df['pos'] == 'ADV')]
    #todas as palavras sem simbolos nem espaços
    df_aux2 = df[df['pos']!='SYM']
    df_aux2 = df_aux2[df_aux2['pos']!='SPACE']
    df_aux2 = df_aux2[df_aux2['pos']!='PUNCT']
    content_density = df_aux.shape[0] / (df_aux2.shape[0]-df_aux.shape[0])
    del df_aux, df_aux2
    metricas['content_density'] = content_density
    
    # Proporção de types de palavras de conteúdo em relação à quantidade de tokens de palavras de conteúdo no texto (id: 64)
    #palavras de conteudo
    df_aux = df[ (df['pos'] == 'PROPN') | (df['pos'] == 'NOUN') | (df['pos'] == 'ADJ') | (df['pos'] == 'AUX') | (df['pos'] == 'VERB') | (df['pos'] == 'ADV')]
    content_word_diversity = df_aux.word.shape[0] / df_aux.shape[0]
    del df_aux
    metricas['content_word_diversity'] = content_word_diversity
    
    # Proporção máxima de palavras de conteúdo em relação à quantidade de palavras das sentenças (id: 65)
    aux_max = 0
    aux_min = 1
    list_content_word = []
    for d in list_df_sent_parse:
        aux = d[(d['pos'] == 'PROPN') | (d['pos'] == 'NOUN') | (d['pos'] == 'ADJ') | (d['pos'] == 'AUX') | (d['pos'] == 'VERB') | (d['pos'] == 'ADV')].shape[0] / d.shape[0]
        if aux > aux_max:
            aux_max=aux
        if aux < aux_min:
            aux_min = aux
        list_content_word.append(aux)
    content_word_max = aux_max
    content_word_min = aux_min
    content_word_standard_deviation = np.std(list_content_word)
    del aux_max, aux_min, d
    metricas['content_word_max'] = content_word_max
    
    # Proporção Mínima de palavras de conteúdo por quantidade de palavras nas sentenças (id: 66)
    metricas['content_word_min'] = content_word_min
    
    # Desvio padrão das proporções entre as palavras de conteúdo e a quantidade de palavras das sentenças (id: 67)
    metricas['content_word_standard_deviation'] = content_word_standard_deviation
    
    # Proporção de types de palavras funcionais em relação à quantidade de tokens de palavras funcionais no texto (id: 68)
    #palavras funcionais
    df_aux = df[(df['pos']=='DET') | (df['pos']=='PROPN') | (df['pos']=='DET') | (df['pos']=='CONJ') | (df['pos']=='SCONJ') | (df['pos']=='CCONJ') | (df['pos']=='PRON') | (df['pos']=='NUM') | (df['pos']=='INTJ') | (df['pos']=='ADP') | (df['pos']=='X')]
    function_word_diversity = df_aux.word.unique().shape[0] / df_aux.shape[0]
    metricas['function_word_diversity'] = function_word_diversity
    
    # Proporção de types de pronomes indefinidos em relação à quantidade de tokens de pronomes indefinidos no texto (id: 69)
    df_aux = df[df['pos'] == 'PRON']
    df_aux = df_aux[df_aux.tag.str.contains('PronType=Ind')]
    
    if df_aux.shape[0]:
        indefinite_pronouns_diversity = df_aux.word.unique().shape[0] / df_aux.shape[0]
    else:
        indefinite_pronouns_diversity = 0
    metricas['indefinite_pronouns_diversity'] = indefinite_pronouns_diversity

    # Proporção de types de substantivos em relação à quantidade de tokens de substantivos no texto (id: 70)
    df_aux = df[(df['pos'] == 'PROPN') | (df['pos'] == 'NOUN')]
    noun_diversity = df_aux.word.unique().shape[0] / df_aux.shape[0]
    del df_aux
    metricas['noun_diversity'] = noun_diversity
    
    # Proporção de types de preposições em relação à quantidade de tokens de preposições no texto (id: 71)
    df_aux = df[df['pos'] == 'ADP']
    preposition_diversity = df_aux.word.unique().shape[0] / df_aux.shape[0]
    del df_aux
    metricas['preposition_diversity'] = preposition_diversity
    
    # Proporção de types de pronomes em relação à quantidade de tokens de pronomes no texto (id: 72)
    df_aux = df[df['pos'] == 'PRON']
    pronoun_diversity = df_aux.word.unique().shape[0] / df_aux.shape[0]
    del df_aux
    metricas['pronoun_diversity'] = pronoun_diversity
    
    # Proporção de types de pontuações em relação à quantidade de tokens de pontuações no texto (id: 73)
    df_aux = df[df['pos'] == 'PUNCT']
    punctuation_diversity = df_aux.word.unique().shape[0] / df_aux.shape[0]
    del df_aux
    metricas['punctuation_diversity'] = punctuation_diversity
    
    # Proporção de types de pronomes relativos em relação à quantidade de tokens de pronomes relativos no texto (id: 74)
    df_aux = df[df['pos'] == 'PRON']
    df_aux = df_aux[df_aux.tag.str.contains('PronType=Rel')]
    relative_pronouns_diversity_ratio = df_aux.word.unique().shape[0] / df_aux.shape[0]
    metricas['relative_pronouns_diversity_ratio'] = relative_pronouns_diversity_ratio
    
    # Proporção de types de verbos em relação à quantidade de tokens de verbos no texto (id: 76)
    df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    verb_diversity = df_aux.word.unique().shape[0] / df_aux.shape[0]
    metricas['verb_diversity'] = verb_diversity
    
    # 7. CONECTIVOS
    
    # Proporção de conectivos aditivos negativos em relação à quantidade de palavras do texto (id: 46)
    count = 0
    for w in lista_conectivos_aditivos_negativos:
        count += txt.count(w)
    add_neg_conn_ratio = count/words
    del count
    metricas['add_neg_conn_ratio'] = add_neg_conn_ratio
    
    # Proporção de conectivos aditivos positivos em relação à quantidade de palavras do texto (id: 47)
    count = 0
    for w in lista_conectivos_aditivos_negativos:
        count += txt.count(w)
    add_pos_conn_ratio = count/words
    del count
    metricas['add_pos_conn_ratio'] = add_pos_conn_ratio
    
    # Proporção de conectivos causais negativos em relação à quantidade de palavras do texto (id: 49)
    count = 0
    for w in lista_conectivos_causais_negativos:
        count += txt.count(w)
    cau_neg_conn_ratio = count/words
    del count
    metricas['cau_neg_conn_ratio'] = cau_neg_conn_ratio
    
    # Proporção de conectivos causais positivos em relação à quantidade de palavras do texto (id: 50)
    count = 0
    for w in lista_conectivos_causais_positivos:
        count += txt.count(w)
    cau_pos_conn_ratio = count/words
    del count
    metricas['cau_pos_conn_ratio'] = cau_pos_conn_ratio
    
    # Proporção de Conectivos em relação à quantidade de palavras do texto (id: 51)
    df_aux = df[(df['pos'] == 'CONJ') | (df['pos'] == 'SCONJ') | (df['pos'] == 'CCONJ')]
    conn_ratio = df_aux.shape[0]/words
    del df_aux
    metricas['conn_ratio'] = conn_ratio
    
    # Proporção de Conectivos Lógicos Negativos em relação à quantidade de palavras do texto (id: 53)
    count = 0
    for w in lista_conectivos_logicos_negativos:
        count += txt.count(w)
    log_neg_conn_ratio = count/words
    del count
    metricas['log_neg_conn_ratio'] = log_neg_conn_ratio
    
    # Proporção de Conectivos Lógicos Positivos em relação à quantidade de palavras do texto (id: 54)
    count = 0
    for w in lista_conectivos_logicos_positivos:
        count += txt.count(w)
    log_pos_conn_ratio = count/words
    del count
    metricas['log_pos_conn_ratio'] = log_pos_conn_ratio
    
    # Proporção do operador lógico E em relação à quantidade de palavras do texto (id: 48)
    count = txt.count(' e ')
    and_ratio = count/words
    del count
    metricas['and_ratio'] = and_ratio
    
    # Proporção do operador lógico SE em relação à quantidade de palavras do texto (id: 52)
    count = txt.count(' se ')
    if_ratio = count/words
    del count
    metricas['if_ratio'] = if_ratio

    # Proporção de Operadores Lógicos em relação à quantidade de palavras do texto (id: 55)
    count = 0
    for w in lista_operadores_logicos:
        count += txt.count(w)
    logic_operators = count/words
    del count
    metricas['logic_operators'] = logic_operators

    # Proporção de palavras que denotam negação em relação à quantidade de palavras do texto (id: 56)
    df_aux = df[(df['pos'] == 'ADV')]
    df_aux = df_aux[df_aux.word.str.contains('|'.join(lista_palavras_negacao))]
    negation_ratio = df_aux.shape[0]/words
    del df_aux
    metricas['negation_ratio'] = negation_ratio
    
    # Proporção do operador lógico OU em relação à quantidade de palavras do texto (id: 57)
    count = txt.count(' ou ')
    or_ratio = count/words
    del count
    metricas['or_ratio'] = or_ratio

    # 8. LÉXICO TEMPORAL
    
    # Proporção de conectivos temporais negativos em relação à quantidade de palavras do texto (id: 150)
    tmp_neg_conn_ratio = txt.count('até que') / words
    metricas['tmp_neg_conn_ratio'] = tmp_neg_conn_ratio
    
    # Proporção de conectivos temporais positivos em relação à quantidade de palavras do texto (id: 151)
    count = 0
    for w in lista_conectivos_temporais_positivos:
        count += txt.count(w)
    tmp_pos_conn_ratio = count/words
    del count
    metricas['tmp_pos_conn_ratio'] = tmp_pos_conn_ratio
    
    # Proporção de verbos auxiliares seguidos de particípio em relação à quantidade de sentenças do texto (id: 141)
    count = 0
    for i in range(df.shape[0]-1):
        if df.iloc[i]['pos'] == 'AUX':
            if 'VerbForm=Part' in df.iloc[i+1]['tag']:
                count+=1
    aux_plus_PCP_per_sentence = count/sentences
    del count
    metricas['aux_plus_PCP_per_sentence'] = aux_plus_PCP_per_sentence
    
    
    # Proporção de Verbos no Pretérito Imperfeito do Indicativo em relação à quantidade de verbos flexionados no texto (id: 142)
    df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    df_aux = df_aux[~df_aux.tag.str.contains("VerbForm=Inf")]
    df_aux2 = df_aux[df_aux.tag.str.contains("Mood=Ind")]
    indicative_imperfect_ratio = df_aux2[df_aux2.tag.str.contains("Tense=Imp")].shape[0] / df_aux.shape[0]
    #del df_aux, df_aux2
    metricas['indicative_imperfect_ratio'] = indicative_imperfect_ratio
    
    # Proporção de Verbos no Pretérito Mais que Perfeito do Indicativo em relação à quantidade de verbos flexionados no texto (id: 143)
    #df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    #df_aux = df_aux[~df_aux.tag.str.contains("VerbForm=Inf")]
    #df_aux2 = df_aux[df_aux.tag.str.contains("Mood=Ind")]
    indicative_pluperfect_ratio = df_aux2[df_aux2.tag.str.contains("Tense=Pqp")].shape[0] / df_aux.shape[0]
    #del df_aux, df_aux2
    metricas['indicative_pluperfect_ratio'] = indicative_pluperfect_ratio
    
    # Proporção de Verbos no Presente do Indicativo em relação à quantidade de verbos flexionados no texto (id: 144)
    #df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    #df_aux = df_aux[~df_aux.tag.str.contains("VerbForm=Inf")]
    #df_aux2 = df_aux[df_aux.tag.str.contains("Mood=Ind")]
    indicative_present_ratio = df_aux2[df_aux2.tag.str.contains("Tense=Pres")].shape[0] / df_aux.shape[0]
    #del df_aux, df_aux2
    metricas['indicative_present_ratio'] = indicative_present_ratio
    
    # Proporção de Verbos no Pretérito Perfeito Simples do Indicativo em relação à quantidade de verbos flexionados no texto (id: 145
    #df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    #df_aux = df_aux[~df_aux.tag.str.contains("VerbForm=Inf")]
    #df_aux2 = df_aux[df_aux.tag.str.contains("Mood=Ind")]
    indicative_preterite_perfect_ratio = df_aux2[df_aux2.tag.str.contains("Tense=Past")].shape[0] / df_aux.shape[0]
    del df_aux, df_aux2
    metricas['indicative_preterite_perfect_ratio'] = indicative_preterite_perfect_ratio
    
    # Proporção de verbos no particípio em relação a todos os verbos do texto (id: 146)
    df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    participle_verbs = df_aux[df_aux.tag.str.contains("VerbForm=Part")].shape[0] / df_aux.shape[0]
    #del df_aux
    metricas['participle_verbs'] = participle_verbs
    
    # Quantidade de diferentes tempos-modos verbais que ocorrem no texto (id: 140)
    lista_tuples = []
    #df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]['tag']
    for s in df_aux:
        mood = re.search(r'^Mood=[A-z]+',s)
        if mood == None:
            continue
        else:
            tense = re.search(r'Tense=[A-z]+',s)
            if tense == None:
                continue
            else:
                mood = mood.group()
                tense = tense.group()
                if (mood, tense) not in lista_tuples:
                    lista_tuples.append((mood, tense))
    verbal_time_moods_diversity = len(lista_tuples)
    try:
        del mood, tense, lista_tuples
    except:
        pass
    metricas['verbal_time_moods_diversity'] = verbal_time_moods_diversity
    
    # Proporção de Verbos no Futuro do Subjuntivo em relação à quantidade de verbos flexionados no texto (id: 147)
    df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    df_aux = df_aux[~df_aux.tag.str.contains("VerbForm=Inf")]
    df_aux2 = df_aux[df_aux.tag.str.contains("Mood=Sub")]
    subjunctive_future_ratio = df_aux2[df_aux2.tag.str.contains("Tense=Fut")].shape[0] / df_aux.shape[0]
    #del df_aux, df_aux2
    metricas['subjunctive_future_ratio'] = subjunctive_future_ratio
    
    # Proporção de Verbos no Pretérito Imperfeito do Subjuntivo em relação à quantidade de verbos flexionados no texto (id: 148)
    df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    #df_aux = df_aux[~df_aux.tag.str.contains("VerbForm=Inf")]
    #df_aux2 = df_aux[df_aux.tag.str.contains("Mood=Sub")]
    subjunctive_imperfect_ratio = df_aux2[df_aux2.tag.str.contains("Tense=Imp")].shape[0] / df_aux.shape[0]
    #del df_aux, df_aux2
    metricas['subjunctive_imperfect_ratio'] = subjunctive_imperfect_ratio
    
    # Proporção de Verbos no Presente do Subjuntivo em relação à quantidade de verbos flexionados no texto (id: 149)
    df_aux = df[(df['pos'] == 'AUX') | (df['pos'] == 'VERB')]
    #df_aux = df_aux[~df_aux.tag.str.contains("VerbForm=Inf")]
    #df_aux2 = df_aux[df_aux.tag.str.contains("Mood=Sub")]
    subjunctive_present_ratio = df_aux2[df_aux2.tag.str.contains("Tense=Pres")].shape[0] / df_aux.shape[0]
    #del df_aux, df_aux2
    metricas['subjunctive_present_ratio'] = subjunctive_present_ratio
    
    # 9. COMPLEXIDADE SINTÁTICA
    
    # Quantidade Média de palavras antes dos verbos principais das orações principais das sentenças (id: 44)
    #ignora o fato de que em frases como 'Ele é inteligente.' O ROOT é o predicativo do sujeito
    lista_indices_root = [df_aux[df_aux.dep == 'ROOT'].id.values[0] for df_aux in list_df_sent_parse if df_aux[df_aux.dep == 'ROOT'].id.values.shape[0]>0]
    words_before_main_verb = np.mean(lista_indices_root)
    del lista_indices_root
    metricas['words_before_main_verb'] = words_before_main_verb
    
    # Quantidade média de adjuntos adverbiais por oração do texto (id: 19)
    #considera os dependencies `case` e advmod com adj_adv e pos AUX e VERB como oracoes
    nr_adj_adv = np.array([df_aux[(df_aux.dep == 'advmod') | (df_aux.dep == 'case')].shape[0] for df_aux in list_df_sent_parse])
    nr_oracoes = np.array([df_aux[(df_aux.pos == 'AUX') | (df_aux.pos == 'VERB')].shape[0] for df_aux in list_df_sent_parse])
    adjunct_per_clause = np.mean(np.array([nr_adj_adv[i]/nr_oracoes[i] for i in range(nr_oracoes.shape[0]) if nr_oracoes[i]>0]))
    del i, nr_adj_adv, nr_oracoes
    metricas['adjunct_per_clause'] = adjunct_per_clause
    
    # Proporção de orações com advérbio antes do verbo principal em relação à quantidade de orações do texto (id: 20)
    nr_adv_antes_verb = 0
    for df_aux in list_df_sent_parse:
        if df_aux[df_aux.pos == "ADV"].shape[0]>0: # se existe adv checa-se se vem antes do verbo
            id_adv = df_aux[df_aux.pos == 'ADV'].id.values[0]
            id_root = df_aux[df_aux.dep == 'ROOT'].id.values[0]
            if id_adv < id_root:
                nr_adv_antes_verb += 1
    adverbs_before_main_verb_ratio = nr_adv_antes_verb / len(list_df_sent_parse)
    # O CORRETO AQUI SERIA FAZER POR ORACAO. FOI FEITO POR FRASE
    
    return(metricas)


print('loading texts...')
df = return_data_frame()
df = df.tail(20)
print(df.shape[0], "minutes")

metrics = []

for txt in df.text.to_list():
    metricsAux = NILCMetrix(txt)
    metrics.append(metricsAux)

dates = df.publish_date.to_list()

def plotMetric(metricName):
    metric = [metrics[i][metricName] for i in range(len(metrics))]
    plt.plot(dates, metric)
    plt.xlabel('Dates')
    plt.ylabel(metricName)
    plt.title(metricName)
    plt.show()
    plt.boxplot(metric)
    plt.title("boxplot - "+metricName)
    plt.show()

# paragraphs
plotMetric("paragraphs")
plotMetric("sentences")
plotMetric("sentences_per_paragraph")
plotMetric("words")
plotMetric("words_per_sentence")
plotMetric("ttr")
plotMetric("content_density")
plotMetric("verb_diversity")