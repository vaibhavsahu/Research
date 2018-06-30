import random
import generateAllQueries as gq
import constants as con
import dataManage as dm
import math
import operator
import time
import os
import arrow
import glob
import re
import graphRelations as gr

def getDataTimes(dataName, hoursBack, timeNow = arrow.utcnow()):
    dataName = 'd' or 'w' or 'r'
    timeNowString = timeNow.format('YYYY_MM_DD@HH_mm_ss')
    #print timeNowString
    #print hoursBack
    #print dataName
    path = con.ROOTdata + 'google' + '\\' + 'real_' + dataName +'*@*.txt'
    #print path
    fileNames = glob.glob(path)
    #print fileNames
    pattern = '_'+dataName+'_(.+?).txt'
    fileTimes = [arrow.get(re.search(pattern, fileName).group(1), 'YYYY_MM_DD@HH_mm_ss')
                     for fileName in fileNames]
    backTime = timeNow.replace(hours=-hoursBack)
    timeNow = arrow.utcnow()
    timeMST = timeNow.to('US/Mountain')
    return [time for time in fileTimes if
       time.timestamp <= timeMST.timestamp and time.timestamp >= backTime.timestamp]

#print getDataTimes('d', 120)

#print [time.format('YYYY_MM_DD@HH_mm_ss') for time in getDataTimes('d', 24)]
# for time in getDataTimes('d', 24):
#     print "INNN"
#     gr.generateGraph(False, time.format('YYYY_MM_DD@HH_mm_ss'))


