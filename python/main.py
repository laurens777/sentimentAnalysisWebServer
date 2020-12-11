# --------------------------------------------------------------------------
# Main entry point for the sentiment analysis scripts
#
# (C) 2020 Laurens Bosman, CMPT383 Fall2020
# Released under the MIT license
# email lbosman@sfu.ca
# -------------------------------------------------------------------------

import os
from bayesModel import runModel
from preprocess import preprocess

# main entrypoint for sentiment analysis
def main(fileName, dataType):
    data = readFile(fileName)
    inputData = preprocess(data)

    result = runModel(inputData, dataType)

    print(result)
    return

# retrieve the data from the temporary file
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