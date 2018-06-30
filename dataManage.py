#write out data
import constants
import arrow
import dataSet
import searches
import csv
import arrow
import os
import matplotlib
import numpy
from scipy import interpolate
import matplotlib.pyplot as plt
from shutil import copyfile
import time

globalNameTimeValue = {}
donePrintNames = []

def writeGoogleCount(printName, timeNow, dataValue):
    writeOneKeywordCount('google', printName, timeNow, dataValue)

def writeArticleCount(printName, timeNow, dataValue):
    writeOneKeywordCount('article', printName, timeNow, dataValue)

def writeTwitterCount(printName, timeNow, dataValue):
    writeOneKeywordCount('twitter', printName, timeNow, dataValue)

#vaibhav
def checkFilesTimestamps():
    '''This routine will look for recently cached files. If files are older than 24 hours, the cache should be updated'''
    files_path = os.path.join(constants.ROOTdata, '*')
    files = sorted(files_path, key=os.path.getctime(), reverse=True)
    current_time = time.time()
    updateCache = round((current_time - os.path.getctime(files[0])) / (3600), 0) < 24 or round((current_time - os.path.getctime(files[1])) / (3600), 0) < 24
    return updateCache


#printName have " " inbetween
    # for each , timeMST.format('YYYY_MM_DD_HH:mm_ss_ZZ'), timeMST.timestamp from the stored time
    #for key, (num1, num2, num3) in mydict.iteritems():
    #    print key, num1, num2, num3
def writeGoogleAllCounts(isTest, nameValueTime, timeNowString, dataType, timePeriod='d'): #timePeriod is either w for week or d for day
    #dataType = 'google'
    dataType = dataType
    if isTest:
        testString = 'test_'
    else: testString = 'real_'
    latestFileName = constants.ROOTdata + dataType + '\\' + testString + timePeriod +'_'+ 'phraseTopics.txt'
    nowFileName = constants.ROOTdata + dataType + '\\' + testString + timePeriod +'_'+ timeNowString +'.txt' #timeNowString
    if not os.path.exists(os.path.dirname(latestFileName)):
        os.makedirs(os.path.dirname(latestFileName))
    #Check if cache needs to be updated, vaibhav


    # needToUpdateCache = True
    # if needToUpdateCache:

    if dataType == 'twitter':
        with open(latestFileName, 'a') as stream:  # previously w was used here as writing mode
            writer = csv.writer(stream, delimiter='\t')
            for printName in sorted(nameValueTime.keys()):
                #if printName not in doneNameValueTime.keys():
                if printName not in donePrintNames:
                    donePrintNames.append(printName)
                    googleCount, dataTime = nameValueTime[printName]
                #doneNameValueTime[printName] = nameValueTime[printName]
                    writer.writerow((printName, googleCount, dataTime.to('US/Mountain').format('YYYY_MM_DD@HH_mm_ss'), dataTime.timestamp))
        #copyfile(nowFileName, latestFileName)
    if dataType == 'google':
        with open(nowFileName, 'w') as stream:#previously w was used here as writing mode
            writer = csv.writer(stream, delimiter = '\t')
            for printName in sorted(nameValueTime.keys()):
                googleCount, dataTime = nameValueTime[printName]
                writer.writerow((printName, googleCount, dataTime.to('US/Mountain').format('YYYY_MM_DD@HH_mm_ss'), dataTime.timestamp))
        print latestFileName
        copyfile(nowFileName, latestFileName)
       
def writeOneKeywordCount(printName, googleCount, dataTime, timePeriod):
    printName = googleCount
    googleCount = timePeriod
    timePeriod = dataTime
    #dataType = 'google' # set google for google data
    dataType = 'google'
    timePeriod = 'd'
    #a little correction in the code


    timeNowString = arrow.utcnow().to('US/Mountain').format('YYYY_MM_DD@HH_mm_ss')
    nowFileName = constants.ROOTdata + dataType + '\\' + timePeriod +'_'+ timeNowString +'.txt' #timeNowString
    #nowFileName = constants.ROOTdata + dataType + '\\' + '+'.join(printName.split(' ')) + '.txt'  # timeNowString
    if not os.path.exists(os.path.dirname(nowFileName)):
        os.makedirs(os.path.dirname(nowFileName))#latestFileName why was it used here

    with open(nowFileName, 'w') as stream:
        writer = csv.writer(stream, delimiter='\t')
        for printName in sorted(globalNameTimeValue.keys()):
            googleCount, dataTime = globalNameTimeValue[printName]
            writer.writerow((printName, googleCount, arrow.utcnow().to('US/Mountain').format('YYYY_MM_DD@HH_mm_ss'), arrow.utcnow().timestamp))

    # with open(nowFileName, 'a') as stream:
    #     writer = csv.writer(stream, delimiter = '\t')
    #     writer.writerow((printName, googleCount, arrow.utcnow().to('US/Mountain').format('YYYY_MM_DD@HH_mm_ss'), arrow.utcnow().timestamp))
        #writer.writerow((printName, googleCount, dataTime.to('US/Mountain').format('YYYY_MM_DD@HH_mm_ss'), dataTime.timestamp))
##
##    
# READ READ READ READ ALL DATA
def readAllCount(isTest, dataType, timePeriod, timeNowString='phraseTopics'):
    #NOTE CHNAGE IN RETURN VALUES, MAY CAUSE BUGS IN ORIGINATING FUNCTIONS
    #returns a dictionary of printName, count, dictionary of printName, timeStamp
    #dataType = 'google'
    dataType = dataType
    #isTest = True
    if isTest:
        testString = 'test_'
    else: testString = 'real_'
    fileName = constants.ROOTdata + dataType + '\\' + testString + timePeriod +'_'+ timeNowString + '.txt'
    #print "FILE NAME + " + fileName
    if os.path.isfile(fileName):
        data = {}
        timeStamps = {}
        with open(fileName,"r") as stream:
            lines = [elem for elem in stream.read().split('\n') if elem]
            for line in lines:
                dataLine = line.replace('\r','').split('\t')
                #print dataLine
                data[dataLine[0]] = int(dataLine[1]) #just first two columns
                timeStamps[dataLine[0]] = int(dataLine[3]) # name and time
        # print 'printing data'
        # print data
        # print 'timeStamps'
        # print timeStamps
        return (data, timeStamps)
    else: #empty array
        print 'error in read data'
        return {}

def readAllCountFraction(isTest, dataType, timeNowString='phraseTopics'):
    #print "Read all count fraction"
    (rawHour, _) = readAllCount(isTest, dataType, 'h', timeNowString)
    #print 'printing raw day'
    #print type(rawDay)
    #print rawDay
    (rawDay, _) = readAllCount(isTest, dataType, 'd', timeNowString)
    #print 'printing raw week'
    #print type(rawDay)
    #print rawWeek
    fraction = {}
    #for queryName, weekCount in rawWeek.iteritems():
    # for queryNameWeekCount in rawWeek: #vaibhav tuple dictionary unpacking
    for queryName, dayCount in rawDay.iteritems():
        if queryName in rawHour:
            hourCount = rawHour[queryName]
            if dayCount == 0:
                fraction[queryName] = 0.0
            else:
                fraction[queryName] = float(hourCount)/float(dayCount)
                if fraction[queryName] <= 0.1:
                    fraction[queryName] = 0.0
                else:
                    fraction[queryName] = 1.0
        else: fraction[queryName] = 0.0
    print fraction
    return fraction
    
#print readAllCountFraction('google')

#price is different
##def writeOnePrice(commoditySymbol, contract, price, closed):
##    timeNow = arrow.utcnow().to('US/Mountain')
##    timeNowString = timeNow.format('YYYY_MM_DD@HH_mm_ss')
##    fileName = constants.ROOTdata + '\\price\\' + contract + '.txt'
##    if not os.path.exists(os.path.dirname(fileName)):
##        os.makedirs(os.path.dirname(fileName))
##    stream = open(fileName, 'a')
##    writer = csv.writer(stream, delimiter = '\t')
##    writer.writerow((timeNowString, timeNow.timestamp, price, closed))


##print readAllCount('google','middle east war')
##z = readAllCount('google','stock market crash')
##a = readAllCount('google','middle east war')
##z = readAllCount('google','stock buy puts')
##a = readAllCount('google','stock buy calls')
##
##z = readAllCount('google','market selloff')
##a = readAllCount('google','russia war')
##
##
##x = z[:,0]
##y= z[:,1]
##f = interpolate.interp1d(x, y)
##
##x0 = a[:,0]
##y0= a[:,1]
##f0 = interpolate.interp1d(x0, y0)
##
##latest = min(x[-1], x0[-1])
##earliest = max(x[0], x0[0])
##
##num = 100
##xx = numpy.linspace(earliest, latest, num)
###print xx
##yy = f(xx)
##yy0 = f0(xx)
##
##plt.plot(xx,yy, 'bo-')
##plt.plot(xx,yy0, 'g.-')
###plt.fill(xx, yy, 'b', xx, yy0, 'r', alpha=0.3)
###plt.imshow(numpy.array((yy,yy0)), interpolation='none',origin='lower')
##plt.show()

        
