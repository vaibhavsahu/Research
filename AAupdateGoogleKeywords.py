#top level commands
import constants as con
import arrow
import searches
import dataManage
import time
#import arrow
import dataManage
import dataSet
import random
import generateAllQueries as gq
#from graphRelations import generateGraph
from random import shuffle
#import visua
#from ipAddress import whatIsMyIPaddress


def updateGoogleKeywords(isTest):
    #get query types and merge
    (_, comTopcomQueryName, comTopTopQueryName, comTopQueryName) = gq.generateQueries()
    allQueryName = comTopcomQueryName + comTopTopQueryName + comTopQueryName
    shuffle(allQueryName) #randomize the order
    nameValueTimeD = {}
    nameValueTimeW = {} #setup memory
    startTime = arrow.utcnow()
    count = 1.0
    for query, printName in allQueryName:
        scrapeWorkedW, countPagesW = scapeOneValue(query, printName, isTest, 'd')
        scrapeWorkedD, countPagesD = scapeOneValue(query, printName, isTest, 'h')
        timeNow = arrow.utcnow()
        timeMST = timeNow.to('US/Mountain')
        if scrapeWorkedD: #and not countPagesW == 0:
            nameValueTimeW[printName] = (countPagesW, timeMST) #timeMST
            nameValueTimeD[printName] = (countPagesD, timeMST)
            # is the value of the day count greater than the 5 day average
            #score = round(100.0*(5.0*float(countPagesD)/countPagesW-1.0))
            #print "%3d; %-28s  %5d(d)"%(round(100.0*count/len(allQueryName)), printName, countPagesD)
            #print "%3d; %-28s  %5d(d) %5d(w) score=%4d"%(round(100.0*count/len(allQueryName)), printName, countPagesD, countPagesW, score) #, address)
            covisualizeunt=count+1
    endTime = arrow.utcnow()
    endTime = endTime.to('US/Mountain')
    timeNowString = endTime.format('YYYY_MM_DD@HH_mm_ss')    
    dataManage.writeGoogleAllCounts(isTest, nameValueTimeD, timeNowString, 'google', 'h', )
    dataManage.writeGoogleAllCounts(isTest, nameValueTimeW, timeNowString, 'google', 'd', )
    #print "%3d queries gathered in %s"%(len(allQueryName), timeDuration(startTime, endTime))
    return endTime

def timeDuration(beforeTime, afterTime):
    change = afterTime.timestamp - beforeTime.timestamp
    timeObject = arrow.get(change)
    return timeObject.format('HH:mm:ss')

def scapeOneValue(query, printName, isTest, timePeriod):
    randomDelayTimes = con.randomDelayTimes()
    scrapeWorked = False
    scapeAttempts = 0
    countPages =  -1
    while scapeAttempts < 8 and not scrapeWorked:
        try:
            countPages, countWords = searches.getQueryData(query, printName, isTest, timePeriod)
            scrapeWorked = True
        except:
            scapeAttempts = scapeAttempts+1
            if scapeAttempts >= 3:
                minDelay = 30
            else:
                minDelay = 5
            if not isTest:
                timeDelay = minDelay + random.uniform(0.0, 3.3)
                time.sleep(timeDelay)
            else: timeDelay = 0.0
            print "GOOGLE ERROR %s Attempt %d Waiting %3.2f"%(printName, scapeAttempts, timeDelay)
        if not isTest and scrapeWorked:
            time.sleep(random.choice(randomDelayTimes) + random.uniform(0.0, 2.0))
    return (scrapeWorked, countPages)
        #address = whatIsMyIPaddress()

#True == 'TEST'
isTest = False
#isTest = True
#timeNow = updateGoogleKeywords(isTest)
# for i in range(0,100):
#     timeNow = updateGoogleKeywords(isTest)
#     #generateGraph(isTest, timeNowString)
#     print "\n\nRESTARTING !!!!!!!!!!!!!!!!!!!!!!!!!"
#     if not isTest:
#         time.sleep(20)
#     time.sleep(10*60)


#print timeNow
#visualize.heatMapQueries('ES', 'd', 1, timeNow)


url = 'http://www.google.com/search?q=intitle:gold+futures+-jewelry*+(strong+buy+OR+go+long+OR+enter+long+OR+-hold*+-short+-sell)+(strong+sell+OR+go+short+OR+shorting+OR+-hold*+-long+-covering+-buy)&tbs=qdr:d'
#url = 'http://www.google.com/search?q=gold+futures+-jewelry*+(strong+buy+OR+go+long+OR+enter+long)+(strong+sell+OR+go+short+OR+shorting+OR+-hold*+-long+-covering+-buy)&tbs=qdr:d'

#searches.getGoogle(url, False)
##while True:
##    updateGoogleKeywords()

##    print "\n"
