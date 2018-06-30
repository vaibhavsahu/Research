# This Python file uses the following encoding: utf-8
import generateAllQueries
import constants
import nltk
from nltk import word_tokenize
import dataManage
import arrow
import string
from datetime import date
import os
import csv

import xlsxwriter

nltk.download('punkt')

globalListPrintNames, _, _, _ = generateAllQueries.generateQueries()
cocoaPrintNames = []
stockMarketPrintNames = []
oilPrintNames = []
goldPrintNames = []
coffeePrintNames = []
hogsPrintNames = []
palladiumPrintNames = []

globalPrintNamesAndCount = {}

# divide the list into different set of lists based on commodities
for (x, y) in globalListPrintNames:
    if x == 'cocoa':
        cocoaPrintNames.append(y)
    if x == 'gold':
        goldPrintNames.append(y)
    if x == 'oil':
        oilPrintNames.append(y)
    if x == 'coffee':
        coffeePrintNames.append(y)
    if x == 'hogs':
        hogsPrintNames.append(y)
    if x == 'palladium':
        palladiumPrintNames.append(y)
    if x == 'stockMarket':
        stockMarketPrintNames.append(y)

#, commoditySymbol
def filterAndUpdatePrintNameCount(tweetText):

    commoditySymbol = ''

    tweetText = tweetText.lower()
    #tweetText = tweetText.translate(None, '()@#?\"')
    #tweetText = tweetText.translate(string.maketrans('', ''), '!()@#?\"')
    # fileName = constants.ROOTdata +  'twitter' + '\\' + 'tweets.csv'
    #
    # with open(fileName, 'a') as stream:
    #     writer = csv.writer(stream)
    #     writer.writerow(tweetText)


    localPrintNames = []

    if 'oil' in tweetText :
        #use goldPrintNames
        print 'oilPrintNames'
        commoditySymbol = 'oil'
        localPrintNames = oilPrintNames
    elif 'gold' in tweetText :
        print 'goldPrintNames'
        commoditySymbol = 'gold'
        localPrintNames = goldPrintNames
    elif 'cocoa' in tweetText:
        print 'cocoaPrintNames'
        commoditySymbol = 'cocoa'
        localPrintNames = cocoaPrintNames
    elif 'copper' in tweetText :
        print 'hogsPrintNames'
        commoditySymbol = 'hogs'
        localPrintNames = hogsPrintNames
    elif 'coffee' in tweetText:
        print 'coffeePrintNames'
        commoditySymbol = 'coffee'
        localPrintNames = coffeePrintNames
    elif 'palladium' in tweetText :
        print 'palladiumPrintNames'
        commoditySymbol = 'palladium'
        localPrintNames = palladiumPrintNames
    else:
        print 'stockMarketPrintNames'
        commoditySymbol = 'stockMarket'
        localPrintNames = stockMarketPrintNames

    nameValueTime = {}
    #create worksheets here
    # filename = filename = constants.ROOTdata +  'twitter' + '\\' +'tweets2excel' + date.today().strftime('%m%d%Y')+ '.xlsx'
    # workbook = xlsxwriter.Workbook(filename)
    # worksheet = workbook.add_worksheet('tweets')
    #worksheet format -> timestamp A1, printNames B1, tweetText C1
    # worksheet.write('A1', 'timestamp')
    # worksheet.write('B1', 'printNames')
    # worksheet.write('C1', 'tweets')
    index = 2
    for locPrintName in localPrintNames:
        #keep a track of printNames
        #if it has been already occured, increment the count
        #else make it zero
        # split the printName at ('_')

        #donePrintNames = []
        isTest = False #just for testing, write printCount 50 as default
        #each time an occurence of printName is found in tweet text, increment it by 1
        #for testing, it can be kept as 50 similar to Google
        printNameCount = 0

        printName = locPrintName

        locPrintName = locPrintName.split('_')

        #trim the commodity symbol from printNames
        locPrintName = locPrintName[1:]

        #if a match is found for printNames in tweettext, update the flag, and increment the printNameCount
        for name in locPrintName:
            # if it is word in one of the dictionaries in futureTopics, marketTopics, or supplyDemand

            if name in constants.marketTopics.keys():
                if '(' in constants.marketTopics[name]:

                    value = constants.marketTopics[name]
                    allList = [i for i in word_tokenize(value)]
                    idxLow = allList.index('(')
                    idxHigh = allList.index(')')
                    nextItem = allList[idxHigh+1]

                    keywordlist = []

                    keywords = [allList[i] for i in range(idxLow + 1, idxHigh) if allList[i] <> 'OR']
                    keywordlist = [j + " " + nextItem for j in keywords]

                    #run a comparison here for tweetext against keywords
                    #tweettext is a string, keywordsList is a list of keywords to be searched for

                    for key in keywordlist:
                        #now key is a list of more granular words
                        found = reduce((lambda x, y: x or y), [True if k in tweetText else False for k in key.split(' ')])
                        if found:#if either of the key from keywordlist is found, end the search.
                            break
                        # for k in key.split(' '):#all words in key should be available in tweetText
                        #     if k in tweetText:
                        #         found = True
                        #     else:
                        #         found = False


                else:
                    value = constants.marketTopics[name].split('OR')
                    includeList = [s for s in value if '-' not in s]
                    excludeList = " ".join([s for s in value if '-' in s]).split(' ') #this list may contain whitespaces as an item
                    excludeList = [i for i in excludeList if i <> '']

                    #scan against includeList
                    for key in includeList:
                        found = reduce((lambda x, y: x or y), [True if k in tweetText else False for k in key.split(' ')])
                        if found:#returned true beacause one of the keywords are found in tweetText
                            break

                    #scan against excludeList
                    for key in excludeList:
                        found = reduce((lambda x, y: x or y), [True if k not in tweetText else False for k in key.split(' ')])
                        if found:#returned true beacause none of the keywords are found in tweetText
                            break


                    #found = found1 and found2


            elif name in constants.supplyAndDemand.keys():
                value = constants.supplyAndDemand[name]
                #contains '('
                if '(' in value:
                    allList = [i for i in word_tokenize(value)]
                    idxLow = allList.index('(')
                    idxHigh = allList.index(')')
                    previousItem = allList[idxLow - 1]

                    keywordlist = []

                    keywords = [allList[i] for i in range(idxLow + 1, idxHigh) if allList[i] <> 'OR']
                    keywordlist = [previousItem + " " + j for j in keywords]

                    for key in keywordlist:
                        #now key is a list of more granular words
                        found = reduce((lambda x, y: x or y), [True if k in tweetText else False for k in key.split(' ')])
                        if found:#if either of the key from keywordlist is found, end the search.
                            break

                #contains '-'
                elif '-' in value:
                    value = constants.supplyAndDemand[name].split('OR')
                    includeList = [s for s in value if '-' not in s]
                    excludeList = [s for s in value if '-' in s]

                    # scan against includeList
                    for key in includeList:
                        found = reduce((lambda x, y: x or y),  [True if k in tweetText else False for k in key.split(' ')])
                        if found:  # returned true beacause one of the keywords are found in tweetText
                            break

                    # scan against excludeList
                    for key in excludeList:
                        found = reduce((lambda x, y: x or y), [True if k not in tweetText else False for k in key.split(' ')])
                        if found:  # returned true beacause none of the keywords are found in tweetText
                            break

                    #found = found1 and found2



                else:# just contain words seperated by ORs
                    includeList = constants.supplyAndDemand[name].split('OR')
                    for key in includeList:
                        #now key is a list of more granular words
                        found = reduce((lambda x, y: x or y), [True if k in tweetText else False for k in key.split(' ')])
                        if found:#if either of the key from keywordlist is found, end the search.
                            break


            else:
                #val = constants.futureTopics.values() # returned value is a list
                #for i in range(0, len(val)):
                if name in constants.futureTopics.keys():
                    value = name
                    #just look for name which is a commodity symbol here, in the tweetText
                    if name in tweetText:
                        found = True

                if name in constants.futureTopics[commoditySymbol]:
                    value = constants.futureTopics[commoditySymbol][name]
                    # print type(value)
                    # returned value is a dictionary
                    # iterate over dictionary
                    # check if it contains  any of keywords in values
                    # check for ORs and ANDs, break it into pair of words based on ANDs and ORs
                    allList = [i for i in word_tokenize(value)]
                    if allList.count('(') >= 2:
                            # process ((a or b ) (c or d)) here
                            # iterate until it is not (( and it is OR
                            # maybe converting list back to word would help
                        value = value.translate(None, "()")
                        keywordlist = value.split('OR')

                        for key in keywordlist:
                            # now key is a list of more granular words
                            found = reduce((lambda x, y: x or y), [True if k in tweetText else False for k in key.split(' ')])
                            if found:  # if either of the key from keywordlist is found, end the search.
                                break


                    elif allList.count('(') == 1:
                            # get index of '(", and of ')'
                            # filter all words between '(' and ')' except OR
                            # save item before '('
                            # join words with previous item and between '(' and ')'
                        idxLow = allList.index('(')
                        idxHigh = allList.index(')')
                        previousItem = allList[idxLow - 1]
                        keywords = [allList[i] for i in range(idxLow+1, idxHigh) if allList[i] <> 'OR']
                        keywordlist = [previousItem + " " + j for j in keywords]

                        # what if there are more keywords before previousItem and after ')'
                        if idxLow - 2 > 0 and idxHigh + 1 < len(allList):
                                keywordlist = [allList[i] for i in range(0, idxLow - 1) if allList[i] <> 'OR']
                                keywordlist = [allList[i] for i in range(idxHigh + 1, len(allList)) if allList[i] <> 'OR']

                        for key in keywordlist:
                            #now key is a list of more granular words
                            found = reduce((lambda x, y: x or y), [True if k in tweetText else False for k in key.split(' ')])
                            if found:#if either of the key from keywordlist is found, end the search.
                                break


                    else:
                            # discard all ORs
                        includeList = [i for i in allList if i != 'OR']
                        for key in includeList:
                            #now key is a list of more granular words
                            found = reduce((lambda x, y: x or y), [True if k in tweetText else False for k in key.split(' ')])
                            if found:#if either of the key from keywordlist is found, end the search.
                                break
        if found:
            printNameCount = printNameCount + 1
        else:
            printNameCount = printNameCount + 0
        if printName in globalPrintNamesAndCount:
            globalPrintNamesAndCount[printName] = printNameCount+1
        else:
            globalPrintNamesAndCount[printName] = 0
        # if printName in donePrintNames:
        #     printNameCount = printNameCount + 1
        # else:
        #     donePrintNames.append(printName)
        if isTest:
           printNameCount = 50

        timeNow = arrow.utcnow().to('US/Mountain')

        if printName not in nameValueTime.keys():
            nameValueTime[printName] = (printNameCount, timeNow)
        else:
            nameValueTime[printName] = (printNameCount+1, timeNow)
        # worksheet.write('A' + str(index), arrow.utcnow().format('YYYY_MM_DD@HH_mm_ss'))
        # worksheet.write('B' + str(index), printName)
        # worksheet.write('C' + str(index), tweetText)
        index = index + 1
        #dataManage.writeGoogleAllCounts(True, nameValueTime, arrow.utcnow().format('YYYY_MM_DD@HH_mm_ss'))
    # for key, value in nameValueTime.iteritems():
    #     count, time = nameValueTime[key]
    #     print count
    #     print key
    #send data to dataManage module for writing to text files
    dataManage.writeGoogleAllCounts(False, nameValueTime, arrow.utcnow().format('YYYY_MM_DD@HH_mm_ss'), 'twitter')
    # workbook.close()


#
#test your method here
# tweetText = 'More Why the rally in @cocoa #futures ? It has only a little to do with #weather.  Though a warm winter, map shows rainfall has been normal  much of W. Africa. Main reason is "demand" and smaller mid-crop hitting the market. Hedgers covered shorts @cocoabutterbf  @business @ReutersAg'
#
# commoditySymbol = 'cocoa'
#
#
# filterAndUpdatePrintNameCount(tweetText, commoditySymbol)
#
# commoditySymbolGold = 'gold'
# tweetTextGold = 'That means you buy gold on the futures market which is just where commodity trading takes place.'
#
# filterAndUpdatePrintNameCount(tweetTextGold, commoditySymbolGold)
#
# #
# commoditySymbolMarket = 'stockMarket'
# tweetTextMarket = 'Stock futures lower as Trump sets stage for trade war: (Reuters) - U.S. stock futures pointed to a fourth straight daily fall on Friday, as investors fretted President Donald Trump had launched a global trade war with his promise to… http://dlvr.it/QJRbLS  #Saudi #Business'
# filterAndUpdatePrintNameCount(tweetTextMarket, commoditySymbolMarket)
