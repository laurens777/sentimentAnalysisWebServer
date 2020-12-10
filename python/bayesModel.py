import pickle
import nltk
from nltk import NaiveBayesClassifier

def trainModel(featureSet, dataType, save=True):
    classifier = NaiveBayesClassifier.train(featureSet)

    if save:
        modelName = "./python/models/" + dataType + "BayesModel.txt"
        with open(modelName, 'wb') as f:
            pickle.dump(classifier, f)

    return classifier

def runModel(data, dataType):
    if dataType == "Twitter":
        with open(".python/models/TwitterBayesModel.txt") as f:
            classifier = pickle.load(f)

        sentiment = classifier.classify(data)