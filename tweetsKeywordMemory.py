import constants
import arrow
import dataManage
#from AAupdateTweetKeywords import getAllKeywords
from FilesToKeywordsList import getAllTwitterKeywords

sampleTime = 10 #time in minutes
class tweetsKeywordMemory:
    
    def __init__(self):
        self.timeCreated = 0;
        #self.keywordsCounts = dict()
        self.keywordsCounts=None
        self.initializeMemory()

    def initializeMemory(self):
        print 'TWEET: initialize Memory'
        self.timeCreated = arrow.utcnow()
        self.keywordsCounts = dict()
        #print '################'
        #print constants.getAllCurrentKeywords()

        for keywords in getAllTwitterKeywords():
        #for keywords in getAllKeywords():
            #print keywords

            #print self.keywordsCounts[keywords]
            self.keywordsCounts[keywords] = 0
        #print '###########'
        #print 'TWEET: Initialization Successful'

    def updateKeywordCounts(self, matchedKeywords):
        #increment the counts for these matches
        #if expired then writeout and start over
        #print 'update {}'.format(matchedKeywords)
        for keywords in matchedKeywords:
            #print keywords vaibhav
            if keywords in self.keywordsCounts:
                self.keywordsCounts[keywords] = self.keywordsCounts[keywords] + 1
            else:
                self.keywordsCounts[keywords] = 0
        #print '***********'
        #print self.keywordsCounts
        if self.expired():
            self.writeOutTweetData()
            self.initializeMemory()

    def expired(self):
        #we have collected enough data over this time 
        timeDifference = arrow.get(arrow.utcnow().timestamp - self.timeCreated.timestamp)
        return timeDifference.minute > sampleTime

    def writeOutTweetData(self):
        print 'TWEET: saving out data'
        timeNow = arrow.utcnow()
        for keywords, count in self.keywordsCounts.iteritems():

            if count >= 0:
                print "Tweets: {} -> {}".format(keywords, count)

            # need to write out the zeros too
            dataManage.writeTwitterCount(keywords, timeNow, count)
        
# test = tweetsKeywordMemory()
# test.updateKeywordCounts(['platinum africa', 'copper Congo', 'gold strike', 'gold mining', 'copper india', 'soybeans planting', 'dollar higher', 'cocoa rain', 'pork short', 'soybeans hit', 'soybeans oil', 'pork export'])
# test.writeOutTweetData()

