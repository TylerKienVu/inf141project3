import pickle
import json
import math
from collections import defaultdict
from recordclass import recordclass
Posting = recordclass("Posting", ["docId", "tf", "tfidf"])

def start():
    index = loadIndex(r"finishedIndex.pkl")
    urlDict = loadURLDictionary(r"C:\Users\Tyler\Documents\GitHub\webpages\WEBPAGES_RAW\bookkeeping.json")
    print("Number of documents in the corpus: " + str(len(urlDict)))
    print("Number of unique tokens: " + str(len(index)))
    startQueryLoop(index, urlDict)

def loadIndex(filePath):
    with open(r"finishedIndex.pkl", 'rb') as f:
        print("Loading index...")
        index = pickle.load(f)
        print("Done.")
        return index

def loadURLDictionary(filePath):
    """
    Opens the json file and returns a dict that can indexed for the file name.
    ex: data[0/0] == <filename>
    """
    with open(filePath) as f:
        data = json.load(f)
        return data

def startQueryLoop(index, urlDict):
    while(True):
        maxQueryReturnSize = getQueryParameter()
        queryWord = input("\nPlease type in a query: ").lower()
        rankedList = rankDocuments(index, queryWord, maxQueryReturnSize)


        if rankedList != []:
            #meta data
            totalLinks = len(rankedList)
            linkCounter = 0
            currentPage = 1
            totalPages = math.ceil(totalLinks/5)

            print("Your query matched " + str(totalLinks) + " pages.")
            print("The following pages match the query (page: " +
                  str(currentPage) + "/" + str(totalPages) + "): ")
            for i in range(len(rankedList)):
                #display first 5 pages
                if linkCounter < 5:
                    totalLinks -= 1
                    linkCounter += 1
                    docId = rankedList[i]
                    print("{:7}: {}".format(docId,urlDict[docId]))

                #ask if user wants to see another page or enter another query
                else:
                    print("\n" + str(totalLinks) + " links left.")
                    nextPage = False
                    while not nextPage:
                        command = input("Next page? [Y] or [N]: ").lower()
                        if command == "y":
                            nextPage = True
                            currentPage += 1
                            linkCounter = 0
                            print("The following pages match the query (page: " +
                                  str(currentPage) + "/" + str(totalPages) + "): ")

                            #print next page because it is still in the loop
                            totalLinks -= 1
                            linkCounter += 1
                            docId = rankedList[i]
                            print("{:7}: {}".format(docId, urlDict[docId]))

                        elif command == "n":
                            break
                        else:
                            print(command + " is an invalid command.")
                    if nextPage == False:
                        break
        else:
            print("There were no pages that match that query.")

def getQueryParameter():
    isValidParameter = False
    while not isValidParameter:
        queryParameter = input(
            "\nPlease specify the max number of results to return (Enter nothing to return all results): ")
        if queryParameter == "":
            return "MAX"
        try:
            convertedParameter = int(queryParameter)
            return convertedParameter
        except ValueError:
            print("\"" + queryParameter + "\" is not a valid parameter. Only integers are allowed.")




def rankDocuments(index, query, maxQueryReturnSize):
    """
    Takes in the query words and returns a list of doc Ids that are ranked based on tf-idf score.
    The score dict will total up the tf-idf's of each doc so that the list of docs can be sorted.
    """
    scoreDict = defaultdict(float)
    rankedList = []
    for word in query.split():
        #grab postings for the token in the query
        postingList = index[word]
        for posting in postingList:
            #puts docId as key and totals up the tf-idf scores for that doc
            scoreDict[posting[0]] += posting[2]

            #puts docId in list to be sorted
            rankedList.append(posting[0])
    
    #sorts the ranked list based on their total tf-idf score
    rankedList.sort(key=lambda x: scoreDict[x], reverse=True)

    #if you want to see the top 10 scores
    # for i in range(10):
    #     print(scoreDict[rankedList[i]])

    if type(maxQueryReturnSize) == int:
        return rankedList[0:maxQueryReturnSize]
    return rankedList



if __name__ == "__main__":
    start()