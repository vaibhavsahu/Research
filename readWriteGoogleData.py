#write out data
import constants
import arrow
import dataSet

#keywords are already + between
def writeOneGoogleCount(commoditySymbol, keywords, googlePageCount):
    #time
    timeStamp = local.timestamp
    timeNow = arrow.utcnow()
    timeNow.to('US/MST')
    #'2013-05-11 13:23:58 -07:00'
    # create time string
    fileName = ROOT + commoditySymbol + '//' + keywords.replace(" ","+")) + '.txt'
    stream = open(fileName, 'a')
    writer = csv.writer(stream, delimiter = '\t')
    writer.writerow(timeNow, googlePageCount)

def readAllGoogleCount(commoditySymbol, keywords)
    thisData = dataSet(commoditySymbol, keywords)
    fileName = ROOT + commoditySymbol + '//' + keywords.replace(" ","+")) + '.txt'
    stream = open(fileName, 'r')
    reader = csv.reader(stream, delimiter = '\t')
    while (timeInstance, googlePageCount = reader.readrow())
      thisData.dataList[timeInstance] = googlePageCount
    return thisData
        
