'''
Ronald Pastori
02/15/17
'''

import sys
import os
import requests # Must be installed with pip3 in the command line
from pathlib import Path
from urllib.parse import urlparse

usage = lambda msg: print(msg, file = sys.stderr)

argc = len(sys.argv)

# Cleanly handles arguments for the sake of modularity and a clean main.
# Very basic functionality for now. I plan on implementing a smarter arg handler
# That can accomodate several different ways the user may pass parameters.
def fetchArgs():
    if argc == 3:
        seedList = sys.argv[1].strip('[]"\'').split(',')
        termList = sys.argv[2].strip('[]"\'').split(',')

        for i in range(len(seedList)):
            seedList[i] = seedList[i].strip(' ')
            if not bool(urlparse.urlparse(seedList[i]).scheme):
                usage("URL list argument contains an invalid URL.")
                return None, None

        for i in range(len(termList)):
            termList[i] = termList[i].strip(' ')

        return seedList, termList
    elif argc == 13: # In the case people enter 12 strings instead of 2 lists
        seedList = []
        termList = []
        for i in range(1, 13):
            arg = sys.argv[i].strip('[]"\', ')
            if i in (1,2):
                seedList.append(arg)
            else:
                termList.append(arg)
        return seedList, termList
    else:
        usage(
            "Please enter two arguments: [list of seed URLS] | [list of ten related terms]"
            )

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

    if argc > 1:
        seedList, termList = fetchArgs()
        if seedList is None or termList is None:
            return

    crawl(seedList, termList, folderPath)

main()
