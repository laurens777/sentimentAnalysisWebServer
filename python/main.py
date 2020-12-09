def main(fileName):
    data = readFile(fileName)

def readFile(fileName):
    data = []

    filePath = "../build/" + fileName
    with open(filePath) as input:
        for line in input:
            data.append(line)
    
    return data


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="main entry point to python sentiment analysis")
    parser.add_argument('fileName', help="file name of the stored data")
    args = parser.parse_args()
    main(args.fileName) 