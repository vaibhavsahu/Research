import constants
import arrow
import dataManage


#This source file seems redundant with tweetsKeywordMemory.py
#Need to confirm this with Dr. Flann
sampleTime = 15
class tweetsKeywordMemory:
    def __init__(self):
        self.initializeMemory()

    def initializeMemory (self):
        self.timeCreated = arrow.utcnow()
        self.keywordsCounts = dict()
        for keywords in constants.getAllCurrentKeywords():
            self.keywordsCounts[keywords] = 0

    def updateKeywordCounts(self, matchedKeywords):
        #increment the counts for these matches
        #if expired then start over
        for keywords in matchedKeywords:
            if keywords in self.keywordsCounts:#vaibhav
                self.keywordsCounts[keywords] = self.keywordsCounts[keywords] + 1
            else:
                self.keywordsCounts[keywords] = 0
        if self.expired():
            self.writeOutTweetData()
        self.initializeMemory(self)

    def expired(self): #we have collected enough data over this time so write out and start over
        timeDifference = arrow.fromtimestamp(arrow.utcnow().timestamp - self.timeCreated.timestamp)
        return timeDifference.minute > sampleTime

    def writeOutTweetData(self):
        timeNow = arrow.utcnow()
        for keywords, count in self.keywordsCounts:
            #print "Tweets: {} -> {}".format(keywords, count)
            dataManage.writeTweetCount(keywords, timeNow, count)
        
