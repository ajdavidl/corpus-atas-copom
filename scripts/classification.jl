using TextAnalysis
using CSV
using DataFrames
using ScikitLearn
using MLDataUtils
using MLBase
using Languages

Mystopwords = ["acordar", "agora", "ainda", "aladi", "alegrar", "além", "antar", "ante", "anthero", "antonio",
    "apenas", "apesar", "apresentação", "aquém", "araújo", "cada", "capitar", "carioca", "carteiro", "contra",
    "corpus", "corrêa", "costa", "daquela", "demais", "diante", "edson", "entanto", "estar", "estevar", "então",
    "feltrim", "final", "finar", "geral", "içar", "ie", "intuito", "le", "luiz", "luzir", "mediante", "meirelles",
    "mercar", "moraes", "necessariamente", "neto", "of", "oficiar", "oliveira", "onde", "ora", "parir", "paulo",
    "pelar", "pesar", "pilar", "pois", "primo", "quadrar", "reinar", "res", "resinar", "reunião", "ser", "sob",
    "sobre", "somente", "sr", "tal", "tais", "tanto", "thomson", "tipo", "todo", "tony", "usecheque", "vasconcelos",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
    "x", "y", "z", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze",
    "treze", "catorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte", "aquela", "aquelas",
    "aquele", "aqueles", "àquela", "àquelas", "daquele", "daqueles", "daquela", "daquelas", "naquele", "naqueles",
    "naquela", "naquelas", "neste", "nesta", "nestes", "nestas", "nisto", "nesse", "nessa", "nesses", "nessas", "nisso",
    "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro",
    "dezembro", "mês", "meses", "ano", "anos"]
Mystopwords = vcat(stopwords(Languages.Portuguese), Mystopwords);

listAtas = readdir("../atas");
corpus = [];

for i in eachindex(listAtas)
    f = open("../atas/" * listAtas[i])
    txt = readlines(f)
    txt = join(txt, " ")
    push!(corpus, txt)
end
println(length(corpus), " atas")

# Load a CSV file with a different delimiter character and skip the headers
df = DataFrame(CSV.File("../decisions.csv", delim=',', header=true));

sort!(df, :meeting);
df = dropmissing(df);
deleteat!(df, findall(df.meeting .== 45 .&& df.selic_rate_target .== 19));
decisions = df.decision;

(train_texts, train_labels), (test_texts, test_labels) = splitobs((corpus, df.decision); at=0.8);

for i in eachindex(train_texts)
    train_texts[i] = lowercase(train_texts[i])
end
return
for i in eachindex(test_texts)
    test_texts[i] = lowercase(test_texts[i])
end

@sk_import feature_extraction.text:TfidfVectorizer
@sk_import svm:LinearSVC
@sk_import ensemble:RandomForestClassifier
@sk_import preprocessing:LabelEncoder

encoder = LabelEncoder()
ScikitLearn.fit!(encoder, df.decision)
train_labels = ScikitLearn.transform(encoder, train_labels)
test_labels = ScikitLearn.transform(encoder, test_labels)


# Use a TfidfVectorizer to convert the text data into a matrix of word counts
vectorizer = TfidfVectorizer(stop_words=Mystopwords, ngram_range=(1, 2), max_df=0.8, min_df=0.2)
train_features = fit_transform!(vectorizer, train_texts)
test_features = ScikitLearn.transform(vectorizer, test_texts)

# Use an SVM classifier to predict the sentiment labels
svm_classifier = LinearSVC(C=1, class_weight="balanced", multi_class="crammer_singer", max_iter=20000)
ScikitLearn.fit!(svm_classifier, train_features, train_labels)
svm_test_preds = ScikitLearn.predict(svm_classifier, test_features)

RF_classifier = RandomForestClassifier(n_estimators=200, class_weight="balanced", bootstrap=false)
ScikitLearn.fit!(RF_classifier, train_features, train_labels)
RF_test_preds = ScikitLearn.predict(RF_classifier, test_features)

function report(y_pred, y_true)
    confMatrix = zeros(3, 3)
    for k in eachindex(y_true)
        i = y_true[k] + 1
        j = y_pred[k] + 1
        confMatrix[i, j] = confMatrix[i, j] + 1
    end
    display(confMatrix)
    acc = (confMatrix[1, 1] + confMatrix[2, 2] + confMatrix[3, 3]) / sum(confMatrix)
    println("Accuracy:", acc)
    precLower = ifelse(sum(confMatrix[:, 1]) == 0, 0, sum(confMatrix[1, 1]) / sum(confMatrix[:, 1]))
    precKeep = ifelse(sum(confMatrix[:, 2]) == 0, 0, sum(confMatrix[2, 2]) / sum(confMatrix[:, 2]))
    precRaise = ifelse(sum(confMatrix[:, 3]) == 0, 0, sum(confMatrix[3, 3]) / sum(confMatrix[:, 3]))
    println("Precision - Lower:", precLower)
    println("Precision - Keep:", precKeep)
    println("Precision - Raise:", precRaise)
    recallLower = ifelse(sum(confMatrix[1, :]) == 0, 0, sum(confMatrix[1, 1]) / sum(confMatrix[1, :]))
    recallKeep = ifelse(sum(confMatrix[2, :]) == 0, 0, sum(confMatrix[2, 2]) / sum(confMatrix[2, :]))
    recallRaise = ifelse(sum(confMatrix[3, :]) == 0, 0, sum(confMatrix[3, 3]) / sum(confMatrix[3, :]))
    println("Recall - Lower:", recallLower)
    println("Recall - Keep:", recallKeep)
    println("Recall - Raise:", recallRaise)

end
println("SVM:")
report(svm_test_preds, test_labels)
println()
println("Random Forest:")
report(RF_test_preds, test_labels)

#println(test_labels)
#println(svm_test_preds)
#println(RF_test_preds)

# TODO:
# Fix hyperparameters