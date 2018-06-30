import numpy as np
import matplotlib.pyplot as plt
import constants
import sys
import dataManage as dm
from scipy import interpolate
import arrow
import os
import time
import generateAllGraphs as gg
import arrow
import tabulate
import math

def getAllData(commoditySymbol, dataSample, hoursBack, timeNow = arrow.utcnow()):
    # dataSample is d or w
    # create two dictionary of name -> list of counts, name -> list of timeStamps
    sampleTimes = gg.getDataTimes(dataSample, hoursBack, timeNow)
    #print sampleTimes
    nameCountList = {}
    nameTimeList = {}
    for timeArrow in sampleTimes:
        #two dictionaries
        nameCounts, nameTimeStamps  = dm.readAllCount(False, dataSample, timeArrow.format('YYYY_MM_DD@HH_mm_ss'))
        #print nameCounts
        for name, count in nameCounts.iteritems():
            #print name
            #print count
            #print nameTimeStamps[name]
            timeStamp = nameTimeStamps[name]
            if name in nameCountList.keys():
                nameCountList[name].append(count)
                nameTimeList[name].append(timeStamp)
            else:
                nameCountList[name] = [count]
                nameTimeList[name] = [timeStamp]
            #CHECK THE TIME ORDER
    return (nameCountList, nameTimeList)

def generateInterpolateFunctions(nameCountList, nameTimeList):
    # returns a nameList and a functionList ealiest, latest timeStamp
    earliest = 0
    latest = sys.maxint #MAY WANT TO USE THE DECISION TIME AND EXTRAPOLATE MISSING DATA FORWARD?
    #OR IF THE DATA SAMPLE IS MISSING DATA AT THE END OR BEGINNING, JUST PUT WHITE
    nameList = []
    dataList = []
    functionList = []
    functionListDelta = []
    # get the name list
    listOfNames = [name for name,_ in nameCountList.iteritems()]
    #print listOfNames
    listOfNames.sort()
    #print listOfNames
    for name in listOfNames:
        try:
            if not len(nameCountList[name]) == 0:
                nameList.append(name)
                y = nameCountList[name]
                #print y
                yDelta = []
                x = nameTimeList[name]
                yLog = [math.log(yOne+2, 2) for yOne in y] #size has log2 hops, count hops
##                if not max(y) == 0:
##                    #y[:] = [yOne/max(y) for yOne in y] #normalize
##                    y[:] = [yOne-np.average(y) for yOne in y] #normalize
##                    #WILL DO SOMETHING MORE COMPLEX ONCE MORE DATA AND VISUALIZATION
                f = interpolate.interp1d(x, y)
                # compute differences #yDelta[y[a + 1] - y[a] for a in range(0, len(y) - 1)]
                # use the new interpolation function to sample Y to generate delat y
                Delta = [y[a + 1] - y[a] for a in range(0, len(y) - 1)]
                print y
                print Delta
                print "\n\n"
                #print yDelta
                #shift
                DeltaShift = [yD - min(Delta) for yD in Delta]
                DeltaLogShift = [math.log(yD+2, 2) for yD in DeltaShift] #size has log2 hops, count hops
                fDelta = interpolate.interp1d(x[1::], Delta)
                earliest = max(earliest, x[0])
                latest = min(latest, x[-1])
                dataList.append(y)
                functionList.append(f)
                functionListDelta.append(fDelta)
        except IndexError:
            #print printName
            #print oneData
            continue
    return (nameList, functionList, functionListDelta, earliest, latest)



##nameCountList, nameTimeList = getAllData('ES', 'd', 7, testTime)
###print nameCountList['stockMarket_change3-_eBola']
###print nameCountList['stockMarket_production']
###print [arrow.get(timeStamp).format('YYYY_MM_DD@HH_mm_ss') for timeStamp in nameTimeList['stockMarket_change3-_eBola']]
##
##nameList, functionList, earliest, latest = generateInterpolateFunctions(nameCountList, nameTimeList)
##print nameList
##print functionList
##print arrow.get(earliest).format('YYYY_MM_DD@HH_mm_ss')
##print arrow.get(latest).format('YYYY_MM_DD@HH_mm_ss')

def getDataMatrix(commoditySymbol, dataSample, hoursBack, dataTime, nowTime=arrow.utcnow()):
    #returns two data arrays data and delta
    nameCountList, nameTimeList = getAllData(commoditySymbol, dataSample, hoursBack, dataTime)
    nameList, functionList, functionListDelta, earliest, latest = generateInterpolateFunctions(nameCountList, nameTimeList)
    minSample = 10 #sample time in minutes
    howMany = hoursBack*(60/minSample) + 1 #for 6 divisions you need 7 time points
##    howMany = 4 #DEBUG
    #resample = np.linspace(earliest, latest, howMany)
    resample = generateSamples(howMany, minSample, latest)
    #print resample
    #CHECK THIS, X IS TIMESTAMP IN INTERPOLATION, MUST USE THE , SAME X FOR VALUE EXTRACTION
    data = np.zeros((len(functionList), howMany))
    dataDelta = np.zeros((len(functionListDelta), howMany))
    #print functionList
    for i in range(len(functionList)):
        for j in range(howMany): 
            data[i, j] = np.nan
            try:
                data[i, j] = functionList[i](resample[j])
                dataDelta[i,j] =functionListDelta[i](resample[j])
            except:
                pass
    return data, dataDelta, resample, nameList
def heatMapQueries(commoditySymbol, dataSample, hoursBack, dataTime, nowTime=arrow.utcnow()):
    # dataSample is d or w
    # get the data
    data, dataDelta, resample, nameList = getDataMatrix(commoditySymbol, dataSample, hoursBack, dataTime, nowTime)
    #print tabulate.tabulate(data)
    #print tabulate.tabulate(dataDelta)
##    plt.plot(resample, data[0, :], 'b.-')
##    plt.plot(resample, data[1, :], 'g.-')
##    plt.plot(resample, data[2, :], 'r.-')
##    plt.plot(resample, data[3, :], 'm.-')
    timeDataString = dataTime.format('YYYY_MM_DD@HH_mm_ss')
    plt.title(constants.symbolToName(commoditySymbol)+'   '+timeDataString, fontsize=12)
    #scale data Delta by log because difference in hops
    #print tabulate.tabulate(dataDelta)
    #fixed pfont
    plt.imshow(data[:,:], interpolation='none',origin='upper',aspect = 0.5) #extent=[0,howMany,0,len(keywordList)])
    plt.gca().grid(False)
    # ticks and time axis are on the hours
    tickTimes = []
    for i in range(len(resample)):
        if (arrow.get(resample[i]).minute%60 == 0): #on the hour
            tickTimes.append(i)
    #plt.gca().axes.get_xaxis().set_ticks(tickTimes)
    #plt.gca().axes.set_xticklabels(map(timeStampToTime, resample[tickTimes]))
    plt.xlabel('Time CDT', fontsize=10)
    #CHECK THE TIME ZONES
    #CHECK THE ORDER BOTH IN X AND Y
    # printName from  -- only have data for
    printNameList = []
    for name in nameList:
        queryTerms = tuple(name.split("_"))
        if len(queryTerms) == 2:
            (futureName, topicName) = queryTerms
            printNameList.append(topicName)
        elif len(queryTerms) == 3:
            (futureName, topicName1, topicName2) = queryTerms
            printNameList.append(topicName1+topicName2.rjust(12))
    plt.gca().axes.get_yaxis().set_ticks(range(0,len(printNameList)))
    plt.gca().axes.set_yticklabels(printNameList)
    plt.gca().tick_params(axis='both', which='major', labelsize=6)
    #file name
    timeNow = arrow.utcnow()
    timeNowString = timeNow.format('YYYY_MM_DD@HH_mm_ss')
    #use the data string as the file name
    dayDataString = dataTime.format('YYYY_MM_DD')
    dayNowString = timeDataString.format('YYYY_MM_DD')
    fileName = constants.ROOTdata + 'heatmaps\\' + dayDataString + '\\' + commoditySymbol + '_Now='+timeNowString + '_DataTime=' + timeDataString +'.png'
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    print fileName
    plt.savefig(fileName, bbox_inches='tight', dpi=200)
    plt.clf()
    return resample

            
def stackPlotData(commoditySymbol, dataSample, hoursBack, dataTime, nowTime=arrow.utcnow()):
    # dataSample is d or w
    # get the data
    data, dataDelta, resample, nameList = getDataMatrix(commoditySymbol, dataSample, hoursBack, dataTime, nowTime)
    if not data:
        return
    timeDataString = dataTime.format('YYYY_MM_DD@HH_mm_ss')
    plt.title(constants.symbolToName(commoditySymbol)+'   '+timeDataString, fontsize=12)
    #scale data Delta by log because difference in hops
    #print tabulate.tabulate(dataDelta)
    #fixed pfont
    plt.stackplot(resample, dataDelta)
    plt.show()
##    plt.gca().grid(False)
##    # ticks and time axis are on the hours
##    tickTimes = []
##    for i in range(len(resample)):
##        if (arrow.get(resample[i]).minute%60 == 0): #on the hour
##            tickTimes.append(i)
##    #plt.gca().axes.get_xaxis().set_ticks(tickTimes)
##    #plt.gca().axes.set_xticklabels(map(timeStampToTime, resample[tickTimes]))
##    plt.xlabel('Time CDT', fontsize=10)
##    #CHECK THE TIME ZONES
##    #CHECK THE ORDER BOTH IN X AND Y
##    # printName from  -- only have data for
##    printNameList = []
##    for name in nameList:
##        queryTerms = tuple(name.split("_"))
##        if len(queryTerms) == 2:
##            (futureName, topicName) = queryTerms
##            printNameList.append(topicName)
##        elif len(queryTerms) == 3:
##            (futureName, topicName1, topicName2) = queryTerms
##            printNameList.append(topicName1+topicName2.rjust(12))
##    plt.gca().axes.get_yaxis().set_ticks(range(0,len(printNameList)))
##    plt.gca().axes.set_yticklabels(printNameList)
##    plt.gca().tick_params(axis='both', which='major', labelsize=6)
##    #file name
##    timeNow = arrow.utcnow().to('US/Mountain')
##    timeNowString = timeNow.format('YYYY_MM_DD@HH_mm_ss')
##    #use the data string as the file name
##    dayDataString = dataTime.format('YYYY_MM_DD')
##    dayNowString = timeDataString.format('YYYY_MM_DD')
##    fileName = constants.ROOTdata + 'heatmaps\\' + dayDataString + '\\' + commoditySymbol + '_Now='+timeNowString + '_DataTime=' + timeDataString +'.png'
##    if not os.path.exists(os.path.dirname(fileName)):
##        os.makedirs(os.path.dirname(fileName))
##    print fileName
##    plt.savefig(fileName, bbox_inches='tight', dpi=200)
##    plt.clf()
##    return resample

def generateSamples(howMany, mins, latest):
    # returns a list of howmany timestamps from now back by mins (minutes)
    timeNow = arrow.get(latest)
    upMinutes = mins-timeNow.minute%mins
    timeNext = timeNow.replace(minutes=+upMinutes) #round up to the next period
    timeNext = timeNext.replace(second=0)
    timeNext = timeNext.replace(microsecond=0)
    timeBack = timeNext.replace(minutes=-mins*(howMany-1)) #because howmany includes +1 for the first and last
    delta = timeNext.timestamp - timeBack.timestamp
    return np.linspace(timeBack.timestamp, timeNext.timestamp, howMany) #because we want start and end

def timeStampToTime(timeStamp):
    return arrow.get(timeStamp).to('US/Central').format('HH:mm') #lower case m is minutes

# TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST
#TEST TEST TEST TEST TEST

#testTime = arrow.get('2014_10_14@01_31_12', 'YYYY_MM_DD@HH_mm_ss') #Three commodities tall
#testTime = arrow.get('2014_09_24@02_38_01', 'YYYY_MM_DD@HH_mm_ss') #three commodities
testTime = arrow.get('2014_10_17@05_33_00', 'YYYY_MM_DD@HH_mm_ss')
testTime = arrow.get('2014_10_19@18_09_34', 'YYYY_MM_DD@HH_mm_ss')
testTime = arrow.get('2014_10_20@07_01_34', 'YYYY_MM_DD@HH_mm_ss')


#heatMapQueries('ES', 'd', 6, testTime)
stackPlotData('ES', 'd', 6, testTime) 

#STOCK MARKET MUST HAVE A SYMBOL
#visualizeData('google', 'ES')

##while True:
##    timeNow = arrow.utcnow()
##    if timeNow.minute % 10 == 0:
##        for commoditySymbol in constants.allCommoditySymbols:
##            #visualizeData('twitter', commoditySymbol)
##            visualizeData('google', commoditySymbol)
##    #time.sleep(60)
    


    
