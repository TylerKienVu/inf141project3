"""
Example of how to open the InvertedIndex file


"""

import pickle
from createIndex import Posting

with open(r"C:\Users\Anthony\Documents\GitHub\inf141project3\index.pkl", 'rb') as f:
    InvertedIndex = pickle.load(f)

print(InvertedIndex)