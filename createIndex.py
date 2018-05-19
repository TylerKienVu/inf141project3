"""This file will take care of parsing the JSON file
to travel through the directory of HTMl files and create the index"""

import json
import pickle
import string
import nltk
import re
import math
from bs4 import BeautifulSoup
from bs4.element import Comment
from recordclass import recordclass

# creates the Posting class
# identical to namedtuple, except it is mutable. This is useful for the rescoring of the
# tf-idf scores of old postings
Posting = recordclass("Posting", ["docId", "tf", "tfidf"])

class indexCreator:
    def __init__(self, webFilesPath, indexPath):
        self.webFilesPath = webFilesPath
        self.indexPath = indexPath
        self.invertedIndex = dict()

    def createIndex(self):
        self._traverseDirectory()
        self._serializeIndex()

    def _openJsonFile(self):
        """
        Opens the json file and returns a dict that can indexed for the file name.
        ex: data[0/0] == <filename>
        """
        with open(self.webFilesPath +"\\bookkeeping.json") as f:
            data = json.load(f)
            return data

    def _traverseDirectory(self):
        """
        Traverses the directories and touches each file in the entire structure.
        """
        jsonData = self._openJsonFile()
        #initialize this class variable for idf score calculating
        self.numberOfDocuments = len(jsonData.keys())
        for key, value in jsonData.items():
            directoryNumber, fileNumber = key.split("/")
            print("Scraping file: " + key)
            self._appendToIndex(directoryNumber, fileNumber, value)

    def _appendToIndex(self, directoryNumber, fileNumber, url):
        """
        Takes the file path and appends the tokens parsed from the file into
        the inverted index.
        """
        with open(self.webFilesPath + "\\" + directoryNumber + "\\" + fileNumber,"rb") as f:
            soup = BeautifulSoup(f,"lxml")
            f.close()
            tokenList = self._filterSoupText(soup.findAll(text=True))
            appendDict = self._createAppendDict(tokenList, directoryNumber + "/" + fileNumber)
            # for k,v in appendDict.items():
            #     print (k + ": " + str(v))
            self._appendDictToIndex(appendDict,len(tokenList))

    def _filterSoupText(self,text):
        """
        Filters the given text and returns a tokenized list
        """
        visibleTextString = filter(self._isVisible, text)
        printableText = ''.join(filter(lambda x: x in string.printable, visibleTextString))
        tokens = map(lambda x: x.lower(), nltk.word_tokenize(printableText))
        cleanString = ' '.join(filter(self._removeSymbols, tokens))
        finalTokens = [x for x in nltk.word_tokenize(cleanString) if x not in nltk.corpus.stopwords.words('english')]
        return finalTokens

    #src: https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    def _isVisible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        if element.isspace():
            return False
        return True

    def _removeSymbols(self,string):
        if (re.match(r'[^\w]', string) != None):
            return False
        return True

    def _createAppendDict(self, tokenList, docId):
        """
        Creates the dict that will contain the information for each token. The function will return
        a dict with key=token, value=(documentId,numberOfTimesTokenAppears).
        """
        appendDict = dict()
        for token in tokenList:
            if token not in appendDict:
                appendDict[token] = (docId,1)
            else:
                appendDict[token] = (docId,appendDict[token][1]+1)
        return appendDict

    def _appendDictToIndex(self,appendDict,numberOfTokens):
        """
        Appends the appendDict to the main index.
        """

        for token in appendDict.keys():
            resultTuple = self._createPosting(token,appendDict,numberOfTokens)
            if token not in self.invertedIndex:
                self.invertedIndex[token] = [resultTuple[0]]
            else:
                #update old Posting tf-idf's
                for i in range(len(self.invertedIndex[token])):
                    currentTf = self.invertedIndex[token][i][1]
                    currentIdf = resultTuple[1]
                    self.invertedIndex[token][i][2] = math.ceil(currentTf * currentIdf * 100)/100
                self.invertedIndex[token].append(resultTuple[0])

    def _createPosting(self,token, appendDict, numberOfTokens):
        """
        Creates and returns a namedtuple with attributes: docId, tf, tfidf

        The inverted index structure is:
        key=token, value=[(docId,tf,tf-idf),(docId,tf,tf-idf)]
        ex: informatics - [(0/5,1.9,2.8),(3/4,2.2,3.4),(4/4,1.1,3.4)]
        note: I chose to store the tf as well as the tf-idf score in order to make it easier to
        rescore the old Postings

        How to calculate tf-idf score:
        TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
        IDF(t) = log(Total number of documents/Number of documents with term t in it)
        tf-idf score = tf x idf
        """

        # calculate tuple items
        tokenTf = math.ceil(appendDict[token][1] / numberOfTokens * 100) / 100  # round to two decimal places
        tokenDocId = appendDict[token][0]

        if token not in self.invertedIndex:
            tokenIdf = math.ceil(math.log(self.numberOfDocuments/1)*100)/100 #because only 1 doc in index
        else:
            tokenIdf = math.ceil(math.log(self.numberOfDocuments / len(
                self.invertedIndex[token]) + 1) * 100) / 100  # divided by number of documents with term in it

        tfidfScore = math.ceil(tokenTf * tokenIdf * 100) / 100

        tupleToInsert = Posting(tokenDocId, tokenTf, tfidfScore)
        return (tupleToInsert,tokenIdf) #return Idf incase old Postings need to be updated

    def _serializeIndex(self):
        """
        Opens the file specified at self.indexPath, Serializes the index into
        the file, and closes the file.
        """
        with open(self.indexPath,"wb") as f:
            pickle.dump(self.invertedIndex,f, pickle.HIGHEST_PROTOCOL)



if __name__ == "__main__":
    # Change file path to path on your computer
    # First path is the directory with the webpages hierarchy
    # Second path is the file that that index will be serialized to

    indexCreatorObject = indexCreator(r"C:\Users\Anthony\Documents\GitHub\WEBPAGES_RAW",
                 r"C:\Users\Anthony\Documents\GitHub\inf141project3\index.pkl")
    indexCreatorObject.createIndex()
