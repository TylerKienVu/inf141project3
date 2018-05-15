"""This file will take care of parsing the JSON file
to travel through the directory of HTMl files and create the index"""

import json
import os
from collections import defaultdict
from pprint import pprint

def openJsonFile(path):
    with open(path) as f:
        data = json.load(f)
        return data

#traverses through every file in the webpages directories
def traverseDirectory(path):
    for root,dirs, files in os.walk(path):
        for file in files:
            if( file in ["bookkeeping.json","bookkeeping.tsv"]):
                continue
            # this is where you would start creating the index
            #appendToIndex(os.path.join(root,file))
            print( os.path.join(root, file))

def appendToIndex(path):
    pass




if __name__ == "__main__":
    # Change file path to path on your computer
    data = openJsonFile(r"C:\Users\tyler\Documents\GitHub\webpages\WEBPAGES_RAW\bookkeeping.json")
    traverseDirectory(r"C:\Users\tyler\Documents\GitHub\webpages\WEBPAGES_RAW")