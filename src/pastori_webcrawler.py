'''
Ronald Pastori
02/15/17
'''

import sys
import os
import requests # Must be installed with pip3 in the command line
from pathlib import Path

def usage(message):
    print(message, file = sys.stderr)

# Cleanly handles arguments for the sake of modularity and a clean main.
# Not currently working. I will use hardcoded values for now and come back to
# this later.
'''
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
            "Please enter three arguments: [list of seed URLS] | [list of ten related terms] | 'Destination folder path'"
            )
'''

def crawl(seedList, termList, folderPath):
    queue = []
    visited = []
    crawledCount = 0
    baseUrl = 'http://en.wikipedia.org/wiki/'
    for url in seedList:
        queue.append(url)

    while queue and crawledCount < 500: # While the queue is not empty
        currURL = queue.pop(0)
        if currURL not in visited:
            resp = requests.get(currURL)
            #print(resp.text)
            visited.append(currURL)

            termCount = 0
            for term in termList:
                if term in resp.text:
                    termCount += 1

            if termCount >= 2:
                # save to directory
                with open(str(folderPath) + '/file' + str(crawledCount) + '.html', 'w') as o:
                    o.write(resp.text)
                crawledCount += 1

def main():
    seedList = ['http://en.wikipedia.org/wiki/Heavy_metal_music', 'http://en.wikipedia.org/wiki/Heavy_metal_genres']
    termList = ['heavy', 'metal', 'music', 'band', 'guitar', 'drums', 'vocals', 'rock and roll', 'black sabbath', 'headbang']
    folderPath = Path('../pages')

    crawl(seedList, termList, folderPath)

main()
