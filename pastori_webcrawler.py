'''
Ronald Pastori
02/15/17
'''

import sys
import os
from pathlib import Path

def usage( message ):
    print( message, file = sys.stderr )

# Cleanly handles arguments for the sake of modularity and a clean main.
def fetchArgs():
    if argc == 4:
        seedList = sys.argv[1]
        terms = sys.argv[2]
        folderPath = Path(sys.argv[3])

        if folderPath.is_dir():
            pass # Good! We can write files here without a problem
        else:
            try:
                os.makedirs(str(folderPath)) # Create directory
            except:
                print("Could not make directory " + str(folderPath), file = sys.stderr)

    else:
        usage(
            "Please enter three arguments: [list of seed URLS] | [list of ten related terms] | [Destination folder path]"
            )

def crawl(seedList, termList, folderPath):
    queue = []
    visited = []
    crawledCount = 0
    for url in seedList:
        queue.append(url)

    while queue and crawledCount < 500: # While the queue is not empty
        pass
