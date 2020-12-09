import string

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk import FreqDist

nltk.download('averaged_perceptron_tagger')

# preprocess takes in a list of strings and outputs a frequency distribution
def preprocess(data):
    tokenizedData = []
    for text in data:
        tokenizedData.append(tokenize(text, "twitter"))
    
    taggedData = []
    for text in tokenizedData:
        taggedData.append(pos_tag(tokenizedData))
    
    finalData = []
    for text in tokenizedData:
        finalData.append(removeStopWords(text))
    
    freqDist = getFrequencyDist(finalData)

def tokenize(data, dataType):
    if dataType == "twitter":
        tokenizer = TweetTokenizer()
        tokens = tokenizer.tokenize(data)
    else:
        tokens = word_tokenize(data)
    
    return tokens
    
def posTag(data):
    taggedData = pos_tag(data)

    return taggedData

def removeStopWords(data):
    cleanData = []
    stopWords = stopwords.words('english')

    for token in data:
        if token not in string.punctuation and token.lower() not in stopWords:
            cleanData.append(token)

    return cleanData

def getFrequencyDist(data):
    tokens = []
    for text in data:
        for token in text:
            tokens.append(token)

    freqDist = FreqDist(tokens)
    print(freqDist.most_common(10))
    return freqDist