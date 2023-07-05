import pandas as pd
import re
import os
import nltk
import numpy as np
import spacy
import xgboost
#import eli5
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm, tree, neural_network, neighbors, ensemble
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV

import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', 200)
pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))
plt.rcParams["figure.figsize"] = (60, 30)
plt.rcParams['figure.dpi'] = 90
plt.rcParams.update({'font.size': 50})

AtasFolder = "../atas"
listAtas = os.listdir(AtasFolder)
corpus = []
meeting = []
for ata in listAtas:
    meeting.append(int(re.search("[0-9]+", ata).group()))
    with open(AtasFolder + "/" + ata, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            lines = ' '.join(lines)
            corpus.append(lines)

print(len(corpus), "atas")
dfCorpus = pd.DataFrame(corpus, index=meeting, columns=["corpus"])
del corpus, meeting

decisions = pd.read_csv("../decisions.csv")
decisions.index = np.int64(decisions.meeting.values)
decisions = decisions["decision"]
decisions = decisions.to_frame(name="decisions")
decisions.value_counts()

dfCorpus = dfCorpus.join(decisions)
del decisions

print('Cleaning data...')

Mystopwords = ['acordar', 'agora', 'ainda', 'aladi', 'alegrar', 'além', 'antar', 'ante', 'anthero', 'antonio', 'apenas', 'apesar', 'apresentação', 'aquém', 'araújo', 'cada', 'capitar', 'carioca', 'carteiro', 'contra', 'corpus', 'corrêa', 'costa', 'daquela', 'demais', 'diante', 'edson', 'entanto', 'estar', 'estevar', 'então', 'feltrim', 'final', 'finar', 'geral', 'içar', 'ie', 'intuito'] + \
    ['le', 'luiz', 'luzir', 'mediante', 'meirelles', 'mercar', 'moraes', 'necessariamente', 'neto', 'of', 'oficiar', 'oliveira', 'onde', 'ora', 'parir', 'paulo', 'pelar', 'pesar', 'pilar', 'pois', 'primo', 'quadrar', 'reinar', 'res', 'resinar', 'reunião', 'ser', 'sob', 'sobre', 'somente', 'sr', 'tal', 'tais', 'tanto', 'thomson', 'tipo', 'todo', 'tony', 'usecheque', 'vasconcelos'] + \
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] + \
    ['um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove', 'vinte'] + \
    ['aquela', 'aquelas', 'aquele', 'aqueles', 'àquela', 'àquelas', 'daquele', 'daqueles', 'daquela', 'daquelas', 'naquele', 'naqueles', 'naquela', 'naquelas', 'neste', 'nesta', 'nestes', 'nestas', 'nisto', 'nesse', 'nessa', 'nesses', 'nessas', 'nisso'] + \
    ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro',
        'dezembro', 'mês', 'meses', 'ano', 'anos'] + [str(i) for i in range(10)] + nltk.corpus.stopwords.words('portuguese')

print("Number of stopwords: ", len(Mystopwords))

corpus = dfCorpus.corpus.to_list()
for i in range(len(corpus)):
    corpus[i] = corpus[i].lower()
    corpus[i] = re.sub('\n', ' ', corpus[i])  # remove newline
    corpus[i] = re.sub('[0-9]+', ' ', corpus[i])  # remove numbers
    corpus[i] = re.sub(r'[^\w\s]', ' ', corpus[i])  # remove punctuation
    corpus[i] = re.sub('º', '', corpus[i])
    corpus[i] = re.sub('ª', '', corpus[i])
    corpus[i] = re.sub('@', '', corpus[i])
    corpus[i] = re.sub('#', '', corpus[i])

print('Lemmatization...')
# large portuguese model
nlp = spacy.load('pt_core_news_lg', disable=['parser', 'ner'])

for i in range(len(corpus)):
    doc = nlp(corpus[i])
    corpus[i] = " ".join([token.lemma_ for token in doc])

# fix wrong lemmas
for i in range(len(corpus)):
    corpus[i] = re.sub("atar", "ata", corpus[i])
    corpus[i] = re.sub("agregar", "agregado", corpus[i])
    corpus[i] = re.sub("atuais", "atual", corpus[i])
    corpus[i] = re.sub("barreirar", "barreira", corpus[i])
    corpus[i] = re.sub("bolhar", "bolha", corpus[i])
    corpus[i] = re.sub("comerciar", "comércio", corpus[i])
    corpus[i] = re.sub("comer", "como", corpus[i])
    corpus[i] = re.sub("conjuntar", "conjunto", corpus[i])
    corpus[i] = re.sub("cifrar", "cifra", corpus[i])
    corpus[i] = re.sub("curvar", "curva", corpus[i])
    corpus[i] = re.sub("demandar", "demanda", corpus[i])
    corpus[i] = re.sub("desalentar", "desalento", corpus[i])
    corpus[i] = re.sub("marginar", "marginal", corpus[i])
    corpus[i] = re.sub("mediano", "mediana", corpus[i])
    corpus[i] = re.sub("mear", "meio", corpus[i])
    corpus[i] = re.sub("mercar", "mercado", corpus[i])
    corpus[i] = re.sub("meter", "meta", corpus[i])
    corpus[i] = re.sub("ofertar", "oferta", corpus[i])
    corpus[i] = re.sub("oitavar", "oitavo", corpus[i])
    corpus[i] = re.sub("orar", "ora", corpus[i])
    corpus[i] = re.sub("parir", "para", corpus[i])
    corpus[i] = re.sub("picar", "pico", corpus[i])
    corpus[i] = re.sub("queda", "quedo", corpus[i])
    corpus[i] = re.sub("redar", "rede", corpus[i])
    corpus[i] = re.sub("resultar", "resultado", corpus[i])
    corpus[i] = re.sub("riscar", "risco", corpus[i])
    corpus[i] = re.sub("segundar", "segundo", corpus[i])
    corpus[i] = re.sub("trazido", "trazer", corpus[i])
    corpus[i] = re.sub("votar", "voto", corpus[i])

dfCorpus["clean_corpus"] = corpus
del corpus, doc, i, nlp


print('Dataset preparation..')

# Divisão dos textos em um conjunto de treinamento e outro de validação
X_train, X_test, y_train, y_test = model_selection.train_test_split(dfCorpus.clean_corpus.to_list(), dfCorpus.decisions.to_list(),
                                                                    test_size=0.30,
                                                                    random_state=100,
                                                                    stratify=dfCorpus.decisions.to_list())
print("Train:", len(X_train), len(y_train))
print("Test:", len(X_test), len(y_test))

# Copy labels
y_train_labels = y_train.copy()
y_test_labels = y_test.copy()

encoder = preprocessing.LabelEncoder()
encoder.fit(dfCorpus.decisions)
y_train = encoder.transform(y_train)
y_test = encoder.transform(y_test)
labels = encoder.classes_
print('Labels:', labels)

max_tokens = 2000
# DTM-TF-IDF
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}',
                             stop_words=Mystopwords,
                             max_df=0.8,
                             min_df=0.1,
                             #ngram_range=(1, 2),
                             max_features=max_tokens)
tfidf_vect.fit(X_train)

print("tfidf:", len(tfidf_vect.get_feature_names_out()), " tokens")

X_train_tfidf = tfidf_vect.transform(X_train)
X_test_tfidf = tfidf_vect.transform(X_test)
list_words = list(tfidf_vect.vocabulary_.keys())


def train_model(classifier, train_x, train_y, test_x, test_y, parameters=None):
    """
    #classifier: sklearn classifier model
    #train_x: train data input (X)
    #train_y: train data output (Y)
    #test_x: test data input (X)
    #test_y: test data output(Y)
    #parameters: classifier's parameters for GridSearch

    """

    if (__name__ == "__main__") & (parameters != None):
        # multiprocessing requires the fork to happen in a __main__ protected
        # block

        # find the best parameters for both the feature extraction and the
        # classifier
        grid_search = GridSearchCV(
            classifier, parameters, n_jobs=-1, verbose=0, cv=5)
        grid_search.fit(train_x, train_y)
        best_parameters = grid_search.best_estimator_.get_params()
        for param_name in sorted(parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))
        predictions = grid_search.best_estimator_.predict(test_x)
        classifier = grid_search.best_estimator_

    else:
        # train the classifier
        classifier.fit(train_x, train_y)
        # make predictions
        predictions = classifier.predict(test_x)

    # calcula a matriz de confusão
    confusionMatrix(predictions, test_y)
    print("\n")  # pula uma linha
    # cria um relatório com base nas previsões realizdas
    classificationReport(predictions, test_y)

    # calcula o kapppa
    kappa = metrics.cohen_kappa_score(test_y, predictions)
    print("Kappa score: {:.3f}\n".format(kappa))
    acc = metrics.accuracy_score(test_y, predictions)
    print("Accuracy score: {:.3f}\n".format(acc))
    f1 = metrics.f1_score(test_y, predictions, average='weighted')
    print("f1 weighted score: {:.3f}\n".format(f1))
    acc_bal = metrics.balanced_accuracy_score(test_y, predictions)
    print("Balanced Accuracy score: {:.3f}\n".format(acc_bal))

    # retorna a acurácia do modelo
    return classifier


def confusionMatrix(predictions, real):
    X = np.array(metrics.confusion_matrix(y_true=real, y_pred=predictions))
    X = pd.DataFrame(X, index=labels, columns=labels)
    print(X)
    return


def classificationReport(predictions, real):
    print(metrics.classification_report(y_true=real,
          y_pred=predictions, target_names=labels))
    return


print('Decision tree...')
# DECISION TREE
nome = "DECISION TREE"
DecisionTreeModel = tree.DecisionTreeClassifier()
parameters_ = {'criterion': ('gini', 'entropy'),
               'splitter': ('best', 'random'),
               'max_depth': (10, 20, 40, 50, None),
               'class_weight': ('balanced', None)
               }

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
DecisionTreeModel = train_model(
    DecisionTreeModel, X_train_tfidf, y_train, X_test_tfidf, y_test, parameters=parameters_)
#tree.plot_tree(DecisionTreeModel, max_depth=3, feature_names=list_words, class_names=labels);
#eli5.show_weights(DecisionTreeModel, top=10, target_names=labels, feature_names=list_words)
#eli5.show_prediction(DecisionTreeModel, X_test[0][:1000], vec=tfidf_vect, target_names=labels)

print('Logistic regression...')
# LOGISTIC REGRESSION
nome = "Logistic Regression"
LogisticRegressionModel = linear_model.LogisticRegression()
parameters_ = {'C': (0.5, 1.0),
               'class_weight': ('balanced', None)}

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
LogisticRegressionModel = train_model(
    LogisticRegressionModel, X_train_tfidf, y_train, X_test_tfidf, y_test, parameters=parameters_)

coefLogReg = pd.DataFrame({'words': list_words,
                           'keep': np.reshape(LogisticRegressionModel.coef_.tolist()[0], (LogisticRegressionModel.coef_.shape[1],)),
                           'lower': np.reshape(LogisticRegressionModel.coef_.tolist()[1], (LogisticRegressionModel.coef_.shape[1],)),
                           'raise': np.reshape(LogisticRegressionModel.coef_.tolist()[2], (LogisticRegressionModel.coef_.shape[1],))})

for i in range(len(labels)):
    print("\n- Words correlated with: "+labels[i]+"\n\t", coefLogReg.sort_values(
        by=labels[i], ascending=False).head(10).words.tolist())

#eli5.show_weights(LogisticRegressionModel, top=10, target_names=labels, feature_names=list_words)
#eli5.show_prediction(LogisticRegressionModel, X_test[0][:1000], vec=tfidf_vect, target_names=labels)

print('SVM..')
# SVM
nome = "SVM"
SVMModel = svm.SVC()
parameters_ = {'C': (0.5, 1.0),
               'kernel': (['linear']),
               'class_weight': ('balanced', None)}

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
SVMModel = train_model(SVMModel, X_train_tfidf, y_train,
                       X_test_tfidf, y_test, parameters=parameters_)


def f_importances(coef, names, nrWords, title):
    imp, names = zip(*sorted(zip(coef, names), reverse=True))
    plt.barh(range(nrWords), imp[:nrWords], align='center')
    plt.yticks(range(nrWords), names[:nrWords])
    plt.title(title)
    plt.xlabel("weight")
    plt.ylabel("words")
    plt.show()


f_importances(SVMModel.coef_[0].todense().tolist()
              [0], list_words, 10, labels[0])
f_importances(SVMModel.coef_[1].todense().tolist()
              [0], list_words, 10, labels[1])
f_importances(SVMModel.coef_[2].todense().tolist()
              [0], list_words, 10, labels[2])

coefSVM = pd.DataFrame({'words': list_words,
                        'keep': np.reshape(SVMModel.coef_.todense().tolist()[0], (SVMModel.coef_.shape[1],)),
                        'lower': np.reshape(SVMModel.coef_.todense().tolist()[1], (SVMModel.coef_.shape[1],)),
                        'raise': np.reshape(SVMModel.coef_.todense().tolist()[2], (SVMModel.coef_.shape[1],))})

for i in range(len(labels)):
    print("\n- Words correlated with: "+labels[i]+"\n\t", coefSVM.sort_values(
        by=labels[i], ascending=False).head(10).words.tolist())

print('Random Forest...')
# RANDOM FOREST
nome = "Random Forest"
RandomForestModel = ensemble.RandomForestClassifier(random_state=100)
parameters_ = {'n_estimators': (50, 75, 100),
               'criterion': ('gini', 'entropy'),
               'max_depth': (20, 40, 50, None),
               'class_weight': ('balanced', 'balanced_subsample', None)
               }

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
RandomForestModel = train_model(
    RandomForestModel, X_train_tfidf, y_train, X_test_tfidf, y_test, parameters=parameters_)

imp = pd.DataFrame(data=RandomForestModel.feature_importances_,
                   index=list_words, columns=['importance'])
#imp.sort_values('importance', ascending=False)

std = np.std([tree.feature_importances_ for tree in RandomForestModel.estimators_],
             axis=0)

indices = np.argsort(RandomForestModel.feature_importances_)[::-1]

nr_words = 20
indices = indices[:nr_words]

plt.rcParams.update({'font.size': 20})

plt.figure(figsize=(15, 10))
plt.title("Random Forest - word importance")
plt.bar(range(nr_words), RandomForestModel.feature_importances_[indices],
        color="g", yerr=std[indices], align="center")
plt.xticks(range(nr_words), pd.Index(list_words)[indices], rotation=75)
plt.xlim([-1, nr_words])
plt.show()

#eli5.show_weights(RandomForestModel, top=10, target_names=labels, feature_names=list_words)
#eli5.show_prediction(RandomForestModel, X_test[0][:1000], vec=tfidf_vect, target_names=labels, top=10)

print('Multinomial Naive Bayes...')
# MULTINOMIAL NAIVE BAYES
nome = "MultinomialNB"
MultinomialNaiveBayes = naive_bayes.MultinomialNB()
parameters_ = {'alpha': (1.0e-10, 0.5, 1.0)}

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
MultinomialNaiveBayes = train_model(
    MultinomialNaiveBayes, X_train_tfidf, y_train, X_test_tfidf, y_test, parameters=parameters_)

print('Gaussian Naive Bayes')
# GAUSSIAN NAIVE BAYES
nome = "GaussianNB"
GaussianNaiveBayes = naive_bayes.GaussianNB()
parameters_ = None

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
GaussianNaiveBayes = train_model(
    GaussianNaiveBayes, X_train_tfidf.toarray(), y_train, X_test_tfidf.toarray(), y_test, parameters=parameters_)

print('KNN')
# KNN
nome = "KNeighbors"
KNeighbors = neighbors.KNeighborsClassifier()
parameters_ = {'n_neighbors': (1, 3, 5, 7, 9),
               'weights': ('uniform', 'distance'),
               'p': (1, 2)}

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
KNeighbors = train_model(
    KNeighbors, X_train_tfidf, y_train, X_test_tfidf, y_test, parameters=parameters_)


print("Stochastic Gradient Descent (SGD)")
nome = "SGDClassifier"
SGDModel = linear_model.SGDClassifier()
parameters_ = {'penalty': ('l1', 'l2', 'elasticnet')}

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
SGDModel = train_model(SGDModel, X_train_tfidf, y_train,
                       X_test_tfidf, y_test, parameters=parameters_)

print("Perceptron")
nome = "Perceptron"
perceptronModel = linear_model.Perceptron()
parameters_ = {'penalty': ('l1', 'l2', 'elasticnet'),
               'class_weight': ('balanced', None)}

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
perceptronModel = train_model(perceptronModel, X_train_tfidf, y_train,
                              X_test_tfidf, y_test, parameters=parameters_)

# EXTREME GRADIENT BOOSTING
print("Extreme Gradient Boosting")
nome = "xgboost.XGBC"
XGBoostModel = xgboost.XGBClassifier(seed=100, random_state=100)
parameters_ = None

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
XGBoostModel = train_model(XGBoostModel, X_train_tfidf,
                           y_train, X_test_tfidf, y_test, parameters=parameters_)

print("Multi-Layer Perceptron")
nome = "MLPClassifier"
MLPModel = neural_network.MLPClassifier(random_state=100, max_iter=1000)
parameters_ = {'activation': ('relu', 'logistic')}

# TF IDF Vectors
print("\n", nome, " - TF-IDF VECTORS")
MLPModel = train_model(MLPModel, X_train_tfidf,
                       y_train, X_test_tfidf, y_test, parameters=parameters_)
