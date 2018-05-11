"""This file will take care of parsing the JSON file
to travel through the directory of HTMl files and create the index"""

import json
from pprint import pprint

def openJsonFile(path):
    with open(path) as f:
        data = json.load(f)
        return data





if __name__ == "__main__":
    # Change file path to path on your computer
    data = openJsonFile(r"C:\Users\tyler\Documents\GitHub\webpages\WEBPAGES_RAW\bookkeeping.json")
    print(data["0/0"])