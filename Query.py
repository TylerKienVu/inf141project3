import pickle
import json
import math
from recordclass import recordclass
Posting = recordclass("Posting", ["docId", "tf", "tfidf"])

def start():
    index = loadIndex(r"finishedIndex.pkl")
    urlDict = loadURLDictionary(r"C:\Users\tyler\Documents\GitHub\webpages\WEBPAGES_RAW\bookkeeping.json")
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
        queryWord = input("\nPlease type in a word to query: ").lower()
        result = index[queryWord]
        if result != []:
            #meta data
            totalLinks = len(result)
            linkCounter = 0
            currentPage = 1
            totalPages = math.ceil(totalLinks/5)

            print("Your query matched " + str(totalLinks) + " pages.")
            print("The following pages match the query (page: " +
                  str(currentPage) + "/" + str(totalPages) + "): ")
            for i in range(len(result)):
                #display first 5 pages
                if linkCounter < 5:
                    totalLinks -= 1
                    linkCounter += 1
                    docId = result[i][0]
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
                            docId = result[i][0]
                            print("{:7}: {}".format(docId, urlDict[docId]))

                        elif command == "n":
                            break
                        else:
                            print(command + " is an invalid command.")
                    if nextPage == False:
                        break
        else:
            print("There were no pages that match that query.")

if __name__ == "__main__":
    start()