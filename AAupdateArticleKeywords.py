#import ahocorasick
import matplotlib
import constants
import urllib2
import re
import time
import constants
import arrow
from datetime import datetime
import BeautifulSoup
import dataManage
import findStrings
from collections import Counter
# searches the articles at bargraph and extracts the mentions of commoditie
# first go to and scrape http://www.barchart.com/futures/marketoverview
#<td><a href="/headlines/story/526332/how-low-are-cotton-prices-going"><img class="thumbnail" src="https://s3.amazonaws.com/news-media/IF/b141b0d62ad234bfac0c177ca0bd9fc2/mseery.jpg"></a><div class="headline"><h1><a href="/headlines/story/526332/how-low-are-cotton-prices-going">How Low Are Cotton Prices Going?</a></h1></div><div class="byline">Michael #Seery - Seery Futures - Thu Jul 03,  2:50PM CDT</div>Great weather equals lower prices (<a href="/headlines/story/526332/how-low-are-cotton-prices-going">full story</a>)<br class="clr"></td>
allKeywordsList = constants.getAllCurrentKeywords()

def updateArticleKeywords():
    urlRoot = 'http://www.barchart.com/futures/news/if'
    headers = {'User-Agent': 'Mozilla'}
    requestRoot = urllib2.Request(urlRoot, None, headers)
    topPage = urllib2.urlopen(requestRoot).read()
    parsed = BeautifulSoup(topPage)
    allLinks = []
    for urlTag in parsed.find_all(href=re.compile("headlines")):
        urlLink = str('http://www.barchart.com' + urlTag['href'])
        allLinks.append(urlLink)
    allMatchedKeywords = list()
    #for urlLink in ['http://www.barchart.com/headlines/story/546163/keep-selling-soybeans-in-my-opinion']: 
    for urlLink in list(set(allLinks)): #remove duplicates
        requestLink = urllib2.Request(urlLink, None, headers)
        #print urlLink
        subPage = urllib2.urlopen(requestLink).read()
        parsedSub = BeautifulSoup(subPage)
        tags = parsedSub.find_all("p")
        theseKeywords = []
        for tag in tags:
            tagString = tag.encode('utf-8') # dont use tag.string!
            #print tagString
            keywordsMatch = findStrings.matchAllKeywords(tagString)
            if keywordsMatch:
                #print keywordsMatch
                theseKeywords.extend(keywordsMatch)
        theseKeywords = list(set(theseKeywords)) #remove duplicates
        allMatchedKeywords.extend(theseKeywords)
        #print theseKeywords
    # save out the data, count duplicates
    timeNow = arrow.utcnow()
    for keywords, value in Counter(allMatchedKeywords).most_common():
        print "Article: {} -> {}".format(keywords, value)
        dataManage.writeArticleCount(keywords, timeNow, value)
    return allMatchedKeywords
                        
while True:
 updateArticleKeywords()
 time.sleep(60)


