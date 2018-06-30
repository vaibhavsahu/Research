import constants
import arrow
import dataManage
import generateAllQueriesTwitter as queryTwitter

sampleTime = 10 #time in minutes
#this file is created to support and extend complex structured queries for Twitter
class tweetsQueriesMemory:
    
    def __init__(self):
        self.timeCreated = 0;
        #self.keywordsCounts = dict()
        self.QueriesCounts=None
        self.initializeMemory()

    def initializeMemory(self):
        print 'TWEET: initialize Memory'
        self.timeCreated = arrow.utcnow()
        self.QueriesCounts = dict()
        #print '################'
        #print constants.getAllCurrentKeywords()
        for query in queryTwitter.generateQueriesTwitter():
            #print keywords
            #print query

            #print self.QueriesCounts[keywords]
            self.QueriesCounts[query] = 0
        #print '###########'
        #print 'TWEET: Initialization Successful'

    # Is it really needed here?? Maybe used later for dummy or test complex structured queries
    def updateKeywordCounts(self):
        #increment the counts for these matches
        #if expired then writeout and start over
        #print 'update {}'.format(matchedKeywords)
        for query in queryTwitter.generateQueriesTwitter():
            #print keywords vaibhav
            #if query in self.QueriesCounts:
            self.QueriesCounts[query] = self.QueriesCounts[query] + 1
        #     else:
        #         self.QueriesCounts[keywords] = 0
        # #print '***********'
        #print self.QueriesCounts
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
        for queries, count in self.QueriesCounts.iteritems():

            if count >= 0:
                print "Tweets: {} -> {}".format(queries, count)
            # need to write out the zeros too
            dataManage.writeTwitterCount(queries, timeNow, count)
        
test = tweetsQueriesMemory()
#test.updateKeywordCounts(['platinum africa', 'copper Congo', 'gold strike', 'gold mining', 'copper india', 'soybeans planting', 'dollar higher', 'cocoa rain', 'pork short', 'soybeans hit', 'soybeans oil', 'pork export'])
test.writeOutTweetData()

