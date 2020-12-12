# --------------------------------------------------------------------------
# Implementation of the Naive Bayes classifier.
#
# (C) 2020 Laurens Bosman, CMPT383 Fall2020
# Released under the MIT license
# email lbosman@sfu.ca
# -------------------------------------------------------------------------

import pickle
import nltk
from nltk import NaiveBayesClassifier
from nltk.corpus import twitter_samples, movie_reviews
from preprocess import preprocess
import os
import random

def trainModel(dataType, save=True):
    if dataType == "Twitter":
        pTweets = twitter_samples.strings('positive_tweets.json')
        nTweets = twitter_samples.strings('negative_tweets.json')
        cleanPTweets = preprocess(pTweets, dataType)
        cleanNTweets = preprocess(nTweets, dataType)
        pDict = []
        nDict = []

        for tweet in cleanPTweets:
            tempDict = {}
            for token in tweet:
                tempDict[token] = True
            pDict.append(tempDict)
        for tweet in cleanNTweets:
            tempDict = {}
            for token in tweet:
                tempDict[token] = True
            nDict.append(tempDict)

        pData = [(tweet, "Positive") for tweet in pDict]
        nData = [(tweet, "Negative") for tweet in nDict]
        dataSet = pData + nData

        random.shuffle(dataSet)
        classifier = NaiveBayesClassifier.train(dataSet)

        if save:
            modelName = "./python/models/" + dataType + "BayesModel.txt"
            with open(modelName, 'wb') as f:
                pickle.dump(classifier, f)

        return classifier
    
    if dataType == "Movie":
        cleanPReviews = []
        cleanNReviews = []
        for file in movie_reviews.fileids('pos'):
            cleanPReviews.append(movie_reviews.words(file))
        for file in movie_reviews.fileids('neg'):
            cleanNReviews.append(movie_reviews.words(file))
        pDict = []
        nDict = []

        for review in cleanPReviews:
            tempDict = {}
            for token in review:
                tempDict[token] = True
            pDict.append(tempDict)
        for review in cleanNReviews:
            tempDict = {}
            for token in review:
                tempDict[token] = True
            nDict.append(tempDict)

        pData = [(review, "Positive") for review in pDict]
        nData = [(review, "Negative") for review in nDict]
        dataSet = pData + nData

        random.shuffle(dataSet)
        classifier = NaiveBayesClassifier.train(dataSet)

        if save:
            modelName = "./python/models/" + dataType + "BayesModel.txt"
            with open(modelName, 'wb') as f:
                pickle.dump(classifier, f)

        return classifier

def runModel(data, dataType):
    inputData = dict([token, True] for token in data[0])
    if os.path.exists("./python/models/" + dataType + "BayesModel.txt"):
        with open("./python/models/" + dataType + "BayesModel.txt", "rb") as f:
            classifier = pickle.load(f)

        sentiment = classifier.classify(inputData)
        return sentiment
    else:
        classifier = trainModel(dataType)
        sentiment = classifier.classify(inputData)
        return sentiment