import math
import pandas as pd
from AAupdateGoogleKeywords import updateGoogleKeywords
import constants
from adjacencyMatrix import *
from PSI import phiGraph
import csv
import arrow
from datetime import datetime

CommodityCombinations = [['gold', 'oil', 'stockMarket'], ['gold'], ['oil','stockMarket'], ['oil'], ['gold', 'stockMarket'], ['stockMarket'], ['gold', 'oil']]
def runOnce(isTest):
    timeNow = updateGoogleKeywords(isTest)
    timeNowString = timeNow.format('YYYY_MM_DD@HH_mm_ss')
    timeStamp = timeNow.timestamp
    # generate all psi data files
    for onlyCommoditiesList in CommodityCombinations:
        psiList = []
        for threshold in constants.thresholdList:
            (nodes, adjacencyDic) = adjacencyMatrix(timeNowString, threshold, onlyCommoditiesList)
            (nodeList, connectMatrix) = adjacencyDicToMatrix(nodes, adjacencyDic)
            displayAdjacencyMatrix(timeNowString, threshold, nodeList, connectMatrix, onlyCommoditiesList)
            psiList.append(phiGraph(connectMatrix, len(nodeList)))
        # write out the data
        commoditiesName = '_'.join(onlyCommoditiesList)
        summaryFile = constants.ROOTdata + "summary" + '_' + commoditiesName + ".txt"
        if not os.path.exists(os.path.dirname(summaryFile)):
            os.makedirs(os.path.dirname(summaryFile))
        with open(summaryFile, 'a') as stream:
            #     #read psi.txt, and price.txt,
            writer = csv.writer(stream, delimiter='\t')
            writer.writerow([timeNowString] + [timeStamp] + psiList)
    for onlyCommoditiesList in CommodityCombinations:
        updateSummaryGraphs(timeNowString, onlyCommoditiesList)


def run():
    while True:
        runOnce(False)
        #updateSummaryGraphs()

def updateSummaryGraphs(timeNowString, onlyCommoditiesList = ['gold', 'oil', 'stockMarket']):
    (lastTime, psiTimeStamps, psiValues) = readSummaryData(onlyCommoditiesList)
    displayPsiVsPriceChange(timeNowString, onlyCommoditiesList)
    plotPsiAndPriceTogether(timeNowString, onlyCommoditiesList=['gold', 'oil', 'stockMarket'])

def getPriceDifferences(lastTime, psiTimeStamps):
    displayMatrix = []
    (priceTimeStamps, spx, oil, gold) = readRawPriceData()
    nowPsiTimeStamp = psiTimeStamps[0]
    (spxPriceLast, oilPriceLast, goldPriceLast) = getPriceAtTime(nowPsiTimeStamp, priceTimeStamps, spx, oil, gold)
    for i in range(1,len(psiTimeStamps)):
        nowPsiTimeStamp = psiTimeStamps[i]
        (spxPriceNow, oilPriceNow, goldPriceNow) = getPriceAtTime(nowPsiTimeStamp, priceTimeStamps, spx, oil, gold)
        displayMatrix.append([spxPriceLast - spxPriceNow, oilPriceLast - oilPriceNow, goldPriceLast - goldPriceNow])
        (spxPriceLast, oilPriceLast, goldPriceLast) = (spxPriceNow, oilPriceNow, goldPriceNow)
    return displayMatrix


#scatter plot and linear regression line
def displayPsiVsPriceChange(timeNowString, onlyCommoditiesList = ['gold', 'oil', 'stockMarket']):
    (lastTime, psiTimeStamps, psiValues) = readSummaryData(onlyCommoditiesList)
    displayMatrix = getPriceDifferences(lastTime, psiTimeStamps)
    displayMatrix = np.transpose(np.array(displayMatrix))

    spxMatrix = displayMatrix[0]
    spxMatrix = np.append(spxMatrix, spxMatrix[-1])
    spxMatrix = [np.absolute(spxMatrix)]
    spxMatrix = np.array(spxMatrix)

    oilmatrix = displayMatrix[1]
    oilmatrix = np.append(oilmatrix, oilmatrix[-1])
    oilmatrix = [np.absolute(oilmatrix)]
    oilmatrix = np.array(oilmatrix)

    goldMatrix = displayMatrix[2]
    goldMatrix = np.append(goldMatrix, goldMatrix[-1])
    goldMatrix = [np.absolute(goldMatrix)]
    goldMatrix = np.array(goldMatrix)

    thresolds = constants.thresholdList
    commodityString = "_".join(onlyCommoditiesList)
    #iterate over each row of psiValues matrix
    for i in range(1, psiValues.shape[0]):

        row = psiValues[i-1:i, :]
        thresold = thresolds[i-1]
        fig, ax = plt.subplots()
        #commodity string, PSI vs Commodity Price, alpha, threshold, corrcoef, value upto 3 places to decimal
        ax.set_title(commodityString + " " + " PSI vs S&P Price" + 'alpha' + " = " +
                     str(thresold)+ " " +
                     "( CC = " +str(np.around(np.corrcoef(row, spxMatrix), decimals=3)[1][0])+ " )")
        fit = np.polyfit(row[0, :], spxMatrix[0, :], deg=1)
        ax.plot(row[0, :], fit[0] * row[0, :] + fit[1], color='red')
        ax.scatter(row, spxMatrix)
        plt.xlabel(commodityString + ' _'+ 'PSI')
        plt.ylabel('S&P Price Change')
        fig.tight_layout()
        fileName = timeNowString + '\\PSI_SP_Price' + "_" + commodityString + '_' + str(thresold) + '_' + timeNowString + '.png'
        if not os.path.exists(os.path.dirname(fileName)):
            os.makedirs(os.path.dirname(fileName))
        plt.savefig(fileName)
        plt.clf()
        #fig.show()


        fig, ax = plt.subplots()
        ax.set_title(commodityString + " " + " PSI vs Oil Price" + 'alpha' + " = " +
                     str(thresold) + " " +
                     "( CC = " + str(np.around(np.corrcoef(row, oilmatrix), decimals=3)[1][0]) + " )")
        fit = np.polyfit(row[0, :], oilmatrix[0, :], deg=1)
        ax.plot(row[0, :], fit[0] * row[0, :] + fit[1], color='red')
        ax.scatter(row, oilmatrix)
        plt.xlabel(commodityString + ' _' + 'PSI')
        plt.ylabel('Oil Price Change')
        fig.tight_layout()
        fileName = timeNowString + '\\PSI_Oil_Price' + "_" + commodityString + '_' + str(thresold) + '_' + timeNowString + '.png'
        if not os.path.exists(os.path.dirname(fileName)):
            os.makedirs(os.path.dirname(fileName))
        plt.savefig(fileName)
        plt.clf()
        #fig.show()
        #
        fig, ax = plt.subplots()
        ax.set_title(commodityString + " " + " PSI vs Gold Price" + 'alpha' + " = " +
                     str(thresold) + " " +
                     "( CC = " + str(np.around(np.corrcoef(row, goldMatrix), decimals=3)[1][0]) + " )")
        fit = np.polyfit(row[0, :], goldMatrix[0, :], deg=1)
        ax.plot(row[0, :], fit[0] * row[0, :] + fit[1], color='red')
        ax.scatter(row, goldMatrix)
        plt.xlabel(commodityString + ' _' + 'PSI')
        plt.ylabel('Gold Price Change')
        fig.tight_layout()
        fileName = timeNowString + '\\PSI_Gold_Price' + "_" + commodityString + '_' + str(thresold) + '_' + timeNowString + '.png'
        if not os.path.exists(os.path.dirname(fileName)):
            os.makedirs(os.path.dirname(fileName))
        plt.savefig(fileName)
        plt.clf()
        #fig.show()



def getPriceAtTime(nowPsiTimeStamp, priceTimes, spx, oil, gold):
    lastPriceTime = priceTimes[0]
    (spx0, oil0, gold0) = (spx[0], oil[0], gold[0])
    for i in range(1,len(priceTimes)):
        if priceTimes[i] > nowPsiTimeStamp:
            return (spx0, oil0, gold0)
        (spx0, oil0, gold0) = (spx[i], oil[i], gold[i])
    return (spx0, oil0, gold0)

def getAllPricesAtTime(nowPsiTimeStamp, priceTimes, spx, oil, gold):
    returnIndex = 0
    for i in range(1,len(priceTimes)):
        if priceTimes[i] > nowPsiTimeStamp:
            returnIndex = i
            break
    return (priceTimes[returnIndex:], spx[returnIndex:], oil[returnIndex:], gold[returnIndex:])

def readRawPriceData():
    marketFutures = "C:\\Users\\flannlab\\Dropbox\\GoogleTrendsFutures\\GoogleTwitterFutures_Vaibhav\\Data\\price.txt"
    df = pd.read_csv(marketFutures, sep='\t', lineterminator='\r', header=None,
    names=['spx', 'oil', 'gold', 'time'], low_memory=False)
    spx1 = [float(i) for i in df['spx'][:-1]]
    spx1.append(spx1[-1])
    df['spx'] = spx1
    timeStamps = [arrow.get(t, 'YYYY_MM_DD_HH_mm_ss').timestamp for t in df['time'][:-1]]
    return (timeStamps, df['spx'][:-1], df['oil'][:-1], df['gold'][:-1])


def displayPriceData(timeNowString, lastTime, psiTimes, startTimeStamp = -1):
    (timeStamps, spx, oil, gold) = readRawPriceData()
    if startTimeStamp == -1:
        startTimeStamp = timeStamps[0]
    (plotTimes, plotSpx, plotOil, plotGold) = getAllPricesAtTime(startTimeStamp, timeStamps, spx, oil, gold)

    timeDates = [datetime.fromtimestamp(stamp).strftime('%b %d') for stamp in plotTimes]
    uniqueTicks = []
    uniqueLables = []
    backDate = timeDates[0]
    for i in range(1,len(timeDates)):
        nowDate = timeDates[i]
        if not backDate == nowDate:
            uniqueTicks.append(plotTimes[i])
            uniqueLables.append(nowDate)
        backDate = nowDate
    print uniqueLables

    #uniqueTimeDates =  np.unique(uniqueTimeDates)


    #spx and time
    fig, ax = plt.subplots()
    plt.title('S&P Price')
    plt.xlabel('Time')
    plt.ylabel('S&P Price')
    plt.xticks(uniqueTicks)
    ax.set_xticklabels(uniqueLables, fontsize=7)
    plt.grid(True)
    plt.plot(plotTimes, plotSpx)
    fileName = timeNowString + '\\' + 'SP_Price' + '_' +  str(lastTime) + '.png'
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    plt.savefig(fileName)
    plt.clf()
    #plt.show()

    # #oil and time
    # fig, ax = plt.subplots()
    # plt.title('Oil Price')
    # plt.xlabel('Time')
    # plt.ylabel('Oil Price')
    # ax.set_xticks(np.arange(len(uniqueTimeDates)))
    # ax.set_xticklabels(uniqueTimeDates, fontsize=7)
    # plt.plot(plotTimes, plotOil)
    # plt.grid(True)
    # fileName = timeNowString + '\\' + 'Oil_Price' + '_' +  str(lastTime) + '.png'
    # if not os.path.exists(os.path.dirname(fileName)):
    #     os.makedirs(os.path.dirname(fileName))
    # #plt.savefig(fileName)
    # #plt.clf()
    # plt.show()
    #
    # #gold and time
    # fig, ax = plt.subplots()
    # plt.title('Gold Price')
    # plt.xlabel('Time')
    # plt.ylabel('Gold Price')
    # ax.set_xticks(np.arange(len(uniqueTimeDates)))
    # ax.set_xticklabels(uniqueTimeDates, fontsize=7)
    # plt.plot(plotTimes, plotGold)
    # plt.grid(True)
    # fileName = timeNowString + '\\' + 'Gold_Price' + '_' +  str(lastTime)  + '.png'
    # if not os.path.exists(os.path.dirname(fileName)):
    #     os.makedirs(os.path.dirname(fileName))
    #plt.savefig(fileName)
    #plt.clf()
    #plt.show()


def readSummaryData(onlyCommoditiesList = ['gold', 'oil', 'stockMarket']):
    times = []
    timeStamps = []
    psiValues = []
    commodityNames = '_'.join(onlyCommoditiesList)
    with open('E:\\Research\\data\\summary_' + commodityNames + '.txt', "r") as stream:
        lines = [elem for elem in stream.read().split('\n') if elem]
        for line in lines:
            dataLine = line.replace('\r', '').split('\t')
            times.append(dataLine[0])
            timeString = dataLine[0]
            timeNow = arrow.get(timeString, 'YYYY_MM_DD@HH_mm_ss')
            timeStamps.append(timeNow.timestamp) #time stamp
            psiValues.append([float(i) for i in dataLine[2:]])
        lastTime = times[:][0]
    #print psiValues
    psiValues = np.transpose(np.array(psiValues))#, dtype=np.float64)
    return (lastTime, timeStamps, psiValues)


def plotPsiAndPriceTogether(timeNowString, onlyCommoditiesList = ['gold', 'oil', 'stockMarket']):
    (lastTime, psiTimes, _) = readSummaryData(onlyCommoditiesList)
    firstPsiTime = psiTimes[0]
    displayPriceData(timeNowString,lastTime, psiTimes, startTimeStamp=firstPsiTime)
    plotPsiAtTime(timeNowString, onlyCommoditiesList)

def plotPsiAtTime(timeNowString, onlyCommoditiesList = ['gold', 'oil', 'stockMarket']):


    timeLabels = []
    # get the psi values
    (lastTime, psiTimes, psiValues) = readSummaryData(onlyCommoditiesList)
    psiNames = [datetime.fromtimestamp(stamp).strftime('%b %d %H %M') for stamp in psiTimes]
    print psiNames
    #get the times at which we have prices
    (allPriceTimes, spx, oil, gold) = readRawPriceData()
    (priceTimes, _,_,_) = getAllPricesAtTime(psiTimes[0], allPriceTimes, spx, oil, gold)
    data = np.zeros((psiValues.shape[0], len(priceTimes)), dtype=float)

    nowPsiIndex = 0

    for i in range(1, len(priceTimes)):
        priceTime = priceTimes[i]
        # if nowPsiIndex == psiValues.shape[1]-1:
        #     break
        if priceTime >= psiTimes[nowPsiIndex+1] and priceTimes[i-1] < psiTimes[nowPsiIndex+1]: # time has moved beyond the next psi value, move on
            nowPsiIndex = nowPsiIndex + 1
            print psiNames[nowPsiIndex]
            print datetime.fromtimestamp(priceTime).strftime('%b %d %H %M')
            print i
            # for j in range(0, psiValues.shape[0]):
            #     # print nowPsiIndex
            #     print data[j, i-1]
            #
            #     print psiValues[j, nowPsiIndex]
        if nowPsiIndex == psiValues.shape[1]-1:
            break
        for j in range(0, psiValues.shape[0]):
                #print nowPsiIndex
            data[j, i] = psiValues[j, nowPsiIndex]
    fig, ax = plt.subplots()
    #all but last column, data[:, :-1]
    im1 = ax.imshow(data, cmap="jet", aspect = 600*5)
    commoditiesString = '_'.join(onlyCommoditiesList)
    thresolds = constants.thresholdList
    ax.set_title(commoditiesString + "Psi vs Price @ " + lastTime)
    plt.xlabel('Time')
    plt.ylabel('PSI')

    timeDates = [datetime.fromtimestamp(stamp).strftime('%b %d') for stamp in priceTimes]
    uniqueTicks = []
    uniqueLables = []
    backDate = timeDates[0]
    firstTimeStamp = priceTimes[0]
    for i in range(1,len(timeDates)):
        nowDate = timeDates[i]
        if not backDate == nowDate:
            uniqueTicks.append(i)
            uniqueLables.append(nowDate)
        backDate = nowDate
    print uniqueLables
    print uniqueTicks
    plt.xticks(uniqueTicks)
    ax.set_xticklabels(uniqueLables, fontsize=7)
    # # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
    # #           rotation_mode="anchor")
    fileName = timeNowString + '\\' + 'psiWithPrice' + '_' + commoditiesString + '_' + timeNowString + '.png'
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    #plt.savefig(fileName)
    fig.tight_layout()
    plt.clf()


run()
#plotPsiAndPriceTogether(timeNowString='2018_05_29@14_09_06', onlyCommoditiesList=['gold', 'oil', 'stockMarket'])
# displayPsiVsPriceChange(onlyCommoditiesList = ['gold', 'oil', 'stockMarket'])
# #plotPsiAtTime(onlyCommoditiesList = ['gold', 'oil', 'stockMarket'])
#displayPsiVsPriceChange(onlyCommoditiesList = ['gold', 'oil', 'stockMarket'])
