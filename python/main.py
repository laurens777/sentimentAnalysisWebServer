import os
import nltk
from nltk.corpus import twitter_samples
from preprocess import preprocess
from bayesModel import trainModel

nltk.download('twitter_samples')

def main(fileName, dataType):
    print("testing")
    if dataType == "Twitter":
        if not os.path.exists("./models/TwitterBayesModel.txt"):
            pTweets = twitter_samples.strings('positive_tweets.json')
            nTweets = twitter_samples.strings('negative_tweets.json')
            cleanPTweets = preprocess(pTweets)
            cleanNTweets = preprocess(nTweets)
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
            dataSet = [(pDict, "Positive"), (nDict, "Negative")]
            classifier = trainModel(dataSet, dataType)

    data = readFile(fileName)
    print(classifier.classify(dict([token, True] for token in data[1])))

def readFile(fileName):
    data = []

    filePath = "./" + fileName
    with open(filePath) as input:
        for line in input:
            data.append(line)
    
    return data


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="main entry point to python sentiment analysis")
    parser.add_argument('fileName', help="file name of the stored data")
    parser.add_argument('dataType', help="data type such as twitter tweet, movie review etc.")
    args = parser.parse_args()
    main(args.fileName, args.dataType) 