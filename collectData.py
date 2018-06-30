#top level commands
import constants
import arrow
import commodityKeywords
import searches
import dataManage
import time
import arrow
import dataManage
import dataSet
import getPrice
#import matplotlib
#import numpy

def gatherAllData():
    for commoditySymbol in constants.allCommoditySymbols:
        thisData = dict()
        for keywordQuery in commodityKeywords.getAllKeywordQuery(commoditySymbol):
            time.sleep(1) #random.randrange(1,3)) #3,10
            count = searches.getGooglePageCount(keywordQuery)
            if (count >= 0):
                thisData[keywordQuery] = count
                print '{}, {}'.format(keywordQuery, count)
        (price, closed) = getPrice.get_last_price(commoditySymbol, 'U', '14')
        #timeStamp = local.timestamp
        timeNow = arrow.utcnow()
        timeMST = timeNow.to('US/Mountain')
        for keywordQuery in thisData.iterkeys():
            print 'keywordQuery ' + keywordQuery
            dataManage.writeOneGoogleCount(commoditySymbol, keywordQuery, timeMST, thisData[keywordQuery])
        dataManage.writeOnePrice(commoditySymbol, 'U', '14', timeMST, price)
        time.sleep(2)

def visualizeOneData(commoditySymbol):
    for keyWordQuery in commodityKeywords.getAllKeywordQuery(commoditySymbol):
        dataManage.readAllGoogleCount(commoditySymbol, keyWordQuery)
    
while True:
    gatherAllData()
    time.sleep(10)
    
            
            
