# --------------------------------------------------------------------------
# Given that the Naive Bayes model cannot be updated this function
# will rerun the training of the model using the data provided by the user.
#
# (C) 2020 Laurens Bosman, CMPT383 Fall2020
# Released under the MIT license
# email lbosman@sfu.ca
# -------------------------------------------------------------------------

import nltk
from nltk.corpus import twitter_samples, movie_reviews
from nltk import NaiveBayesClassifier
from preprocess import preprocess
import random
import pickle

def correctModel(fName, dataType, correction):
    if dataType == "Twitter":
        pTweets = twitter_samples.strings('positive_tweets.json')
        nTweets = twitter_samples.strings('negative_tweets.json')
        cleanPTweets = preprocess(pTweets, dataType)
        cleanNTweets = preprocess(nTweets, dataType)

        data = []
        filePath = "./" + fName
        with open(filePath) as input:
            for line in input:
                data.append(line)

        inputData = preprocess(data, dataType)

        if correction == "positive":
            for i in inputData:
                cleanPTweets.append(i)
        else:
            for i in inputData:
                cleanNTweets.append(i)

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

        modelName = "./python/models/" + dataType + "BayesModel.txt"
        with open(modelName, 'wb') as f:
            pickle.dump(classifier, f)
    
    if dataType == "Movie":
        cleanPReviews = []
        cleanNReviews = []
        for file in movie_reviews.fileids('pos'):
            cleanPReviews.append(movie_reviews.words(file))
        for file in movie_reviews.fileids('neg'):
            cleanNReviews.append(movie_reviews.words(file))

        data = []
        filePath = "./" + fName
        with open(filePath) as input:
            for line in input:
                data.append(line)

        inputData = preprocess(data, dataType)
        if correction == "positive":
            for i in inputData:
                cleanPReviews.append(i)
        else:
            for i in inputData:
                cleanNReviews.append(i)

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

        modelName = "./python/models/" + dataType + "BayesModel.txt"
        with open(modelName, 'wb') as f:
            pickle.dump(classifier, f)

    return

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="main entry point to python sentiment analysis")
    parser.add_argument('fileName', help="file name of the stored data.")
    parser.add_argument('dataType', help="data type such as twitter tweet, movie review etc.")
    parser.add_argument('correction', help="Correct sentiment classification for the data.")
    args = parser.parse_args()
    correctModel(args.fileName, args.dataType, args.correction) 