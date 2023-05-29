using TextAnalysis
using CSV
using DataFrames
using ScikitLearn
using MLDataUtils
using MLBase
using Languages

Mystopwords = stopwords(Languages.Portuguese);

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
#println(df)
decisions = df.decision;
d = Dict("lower" => -1, "keep" => 0, "raise" => 1);
labels = [d[i] for i in decisions];
#println(labels)
#println(length(corpus))
#println(length(labels))

(train_texts, train_labels), (test_texts, test_labels) = splitobs((corpus, labels); at=0.8);
#println(typeof(train_texts))
#println(typeof(test_texts))

for i in eachindex(train_texts)
    train_texts[i] = lowercase(train_texts[i])
end
return
for i in eachindex(test_texts)
    test_texts[i] = lowercase(test_texts[i])
end

@sk_import feature_extraction.text:CountVectorizer
@sk_import svm:SVC
@sk_import ensemble:RandomForestClassifier

# Use a CountVectorizer to convert the text data into a matrix of word counts
vectorizer = CountVectorizer(stop_words=Mystopwords, ngram_range=(1, 2))
train_features = fit_transform!(vectorizer, train_texts)
test_features = ScikitLearn.transform(vectorizer, test_texts)

# Use an SVM classifier to predict the sentiment labels
svm_classifier = SVC(C=0.8)
ScikitLearn.fit!(svm_classifier, train_features, train_labels)
svm_test_preds = ScikitLearn.predict(svm_classifier, test_features)

RF_classifier = RandomForestClassifier(n_estimators=200)
ScikitLearn.fit!(RF_classifier, train_features, train_labels)
RF_test_preds = ScikitLearn.predict(RF_classifier, test_features)

function report(y_pred, y_true)
    confMatrix = zeros(3, 3)
    for k in eachindex(y_true)
        #labels are -1, 0 and 1
        i = y_true[k] + 2
        j = y_pred[k] + 2
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