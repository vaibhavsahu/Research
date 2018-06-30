#gets the latest price of this commodity from the web
import urllib2
import re
import time
import constants
import arrow
from datetime import datetime
from sys import argv
from bs4 import BeautifulSoup
import dataManage

#http://www.barchart.com/quotes/futures/KCU14
#<span class="last" id="dtaLast">182.05s</span>

#contract = 'KCU14'

def updateAllCommodityPrices():
    for commoditySymbol in constants.allCommoditySymbols:
        print 'in updateAllCommoditiesPrices'
        print commoditySymbol
        updateLastPrices(commoditySymbol)
    
def updateLastPrices(commoditySymbol):
    # scrapes the prices and update the files
    urlRoot = 'http://www.barchart.com/commodityfutures/'
    url = urlRoot + constants.symbolToName(commoditySymbol) + '_Futures/' + commoditySymbol
    headers = {'User-Agent': 'Mozilla'}
    req = urllib2.Request(url, None, headers)
    results = urllib2.urlopen(req).read()
    parsed = BeautifulSoup(results, 'html.parser')
    try:
        for contractName in contractNames(commoditySymbol):
            print contractName
            tagId = 'dt1_' + contractName + '_last'
            priceTag = parsed.find("td", id=tagId)
            if priceTag is None:
               continue
            priceString = priceTag.string.replace(",","")
            if priceString.find("s"): #market closed
                priceString = priceString.replace("s","")
                closed = True
            else:
                closed = False
            try:
                price = float(priceString.replace("s",""))
                dataManage.writeOnePrice(commoditySymbol, contractName, price, closed)
            except ValueError:
                price = -1
    except:
        pass

def allContractNames():
    allContracts = []
    for commoditySymbol in constants.allCommoditySymbols:
        for contract in contractNames(commoditySymbol):
            allContracts = allContracts + [contract]
    print 'allContracts'
    print allContracts
                                      
def contractNames(commoditySymbol, howMany=4):
    #returns a list of the next contract names
    nowTime = arrow.utcnow()
    nowYear = nowTime.year
    nowMonth = nowTime.month
    count = 1
    contracts = []
    for year in range(nowYear, nowYear+2):
        for month in constants.symbolToMonths(commoditySymbol):
            #ignore the first months of this year
            if year == nowYear and constants.monthNumber(month) < nowMonth:
                continue
            # keep collecting
            if count <= howMany:
                contracts = contracts + [commoditySymbol + month + str(year % 100)]
            count = count+1
    print '*************'
    print contracts
    return contracts

while True:
 updateAllCommodityPrices()
 time.sleep(10)
            
#updateLastPrices('GC')
#<td id="dt1_GCY00_last" align="right" class="ds_last qb_shad" nowrap="nowrap" style="background-color: rgb(255, 255, 161);">1,320.68</td>
#<td id="dt1_GCN14_last" align="right" class="ds_last qb_line" nowrap="nowrap">1,320.1</td>
#<td id="dt1_GCQ14_last" align="right" class="ds_last qb_shad" nowrap="nowrap">1,321.8</td>
