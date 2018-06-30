#import ahocorasick
import constants
import urllib2
import re
import time
import constants
import arrow
from datetime import datetime
from bs4 import BeautifulSoup
import dataManage
import getPrice
import findStrings
from collections import Counter
# searches the articles at bargraph and extracts the mentions of commoditie
# first go to and scrape http://www.barchart.com/futures/marketoverview
#<td><a href="/headlines/story/526332/how-low-are-cotton-prices-going"><img class="thumbnail" src="https://s3.amazonaws.com/news-media/IF/b141b0d62ad234bfac0c177ca0bd9fc2/mseery.jpg"></a><div class="headline"><h1><a href="/headlines/story/526332/how-low-are-cotton-prices-going">How Low Are Cotton Prices Going?</a></h1></div><div class="byline">Michael #Seery - Seery Futures - Thu Jul 03,  2:50PM CDT</div>Great weather equals lower prices (<a href="/headlines/story/526332/how-low-are-cotton-prices-going">full story</a>)<br class="clr"></td>
def updateArticleKeywords():
    urlRoot = 'http://www.barchart.com/futures/news/if'
    headers = {'User-Agent': 'Mozilla'}
    requestRoot = urllib2.Request(urlRoot, None, headers)
    topPage = urllib2.urlopen(requestRoot).read()
    timeNow = arrow.utcnow()
    parsed = BeautifulSoup(topPage)
    allLinks = []
    for urlTag in parsed.find_all(href=re.compile("headlines")):
        urlLink = str('http://www.barchart.com' + urlTag['href'])
        allLinks = allLinks + [urlLink]
    allKeywords = list()
    #for urlLink in ['http://www.barchart.com/headlines/story/546163/keep-selling-soybeans-in-my-opinion']: 
    for urlLink in list(set(allLinks)): #remove duplicates
        requestLink = urllib2.Request(urlLink, None, headers)
        print urlLink
        subPage = urllib2.urlopen(requestLink).read()
        parsedSub = BeautifulSoup(subPage)
        tags = parsedSub.find_all("p")
        theseKeywords = []
        for keywords in constants.getAllCurrentKeywords():
            count = 0
            for tag in tags:
                tagString = tag.encode('utf-8') # dont use tag.string!
                #print tagString
                keywordsMatch = findStrings.keywordsInString(tagString, keywords)
                if keywordsMatch:
                    #print keywords
                    theseKeywords = theseKeywords + [keywords]
        theseKeywords = list(set(theseKeywords))
        for key in theseKeywords:
            allKeywords = allKeywords + [key]
        print theseKeywords
    # save out the data, count duplicates
    for keys, value in Counter(allKeywords).most_common():
        print "{} -> {}".format(keys, value)
        dataManage.writeArticleCount(keys, timeNow, value)
    return allKeywords
#for keys, v in Counter(allKeywords).most_common():
#    print "{} -> {}".format(keys, v)
##    for keywords in allKeyWords:
##        writeArticleCount(keywordQuery, timeNow, articleCount)
        
##while True:
##   updateArticleKeywords()
##   time.sleep(60)
                        
allKeywords = updateArticleKeywords()                    

##>>> import ahocorasick
##>>> tree = ahocorasick.KeywordTree()
##>>> tree.add("alpha")          
##>>> tree.add("alpha beta")
##>>> tree.add("gamma")
##>>>
##>>> tree.make()
##>>>
##>>> tree.search("I went to alpha beta the other day to pick up some spam")    
                

        
    
#identify each author and the link to the article, follow the link and scrape the content off. Then search first search for each commodity name, if it exists
#then search for each keyword and count them.
