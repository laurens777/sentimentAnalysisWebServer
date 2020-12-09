import pickle
import nltk
from nltk import NaiveBayesClassifier

def trainModel(featureSet, dataType, save=True):
    classifier = NaiveBayesClassifier.train(featureSet)

    if save:
        modelName = dataType + "BayesModel.txt"
        file = open(modelName, 'wb')
        pickle.dump(classifier, file)
        file.close()
