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
    limit = 500
    baseUrl = 'http://en.wikipedia.org/wiki/'
    for url in seedList:
        queue.append(url)

    print("Starting the webcrawl process:")
    print("... crawling...")
    while queue and crawledCount < limit: # While the queue is not empty
        currURL = queue.pop(0)
        if currURL not in visited:
            resp = requests.get(currURL)
            visited.append(currURL)

            termCount = 0
            for term in termList:
                if term.lower() in resp.text.lower():
                    termCount += 1
                if termCount == 2: # I'll remove this if I ever need to increase
                    break # the threshold or measure precision. For now this is
                    # to save runtime

            if termCount >= 2:
                # save to directory
                with open(str(folderPath) + '/page' + str(crawledCount) + '.html', 'w') as o:
                    o.write(resp.text)
                crawledCount += 1

            # Looks for new URLs linked in the page.
            # For now, I'm limited to Wikipedia pages, which makes my job easier
            pageLocation = 'href="/wiki/'
            for line in resp.iter_lines():
                idx = str(line).find(pageLocation)
                if idx != -1:
                    urlPiece = str(line)[idx + len(pageLocation):] # slice of line
                    tempList = urlPiece.split('"') # separates the part I actually
                    urlPiece = tempList[0] # from the trailing junk
                    queue.append(baseUrl + urlPiece)

    print("All done! Check the", str(folderPath), "directory for the top", limit, "results.")

def main():
    seedList = ['http://en.wikipedia.org/wiki/Heavy_metal_music', 'http://en.wikipedia.org/wiki/Heavy_metal_genres']
    termList = ['heavy', 'metal', 'music', 'band', 'guitar', 'drums', 'vocals', 'rock and roll', 'black sabbath', 'headbang']
    folderPath = Path('../pages')

    crawl(seedList, termList, folderPath)

main()
