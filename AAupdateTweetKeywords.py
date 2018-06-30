import json
import tweepy
import findStrings
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import constants
import arrow
import dataManage
import findStrings
import tweetsKeywordMemory
import getTwitterUsers
import twitterAuthentication
import threading
from TwitterFilters import filterAndUpdatePrintNameCount





#keys for Authentication
consumer_key= 'ytwg4fSktfnqbktUIkhlaWggQ'
consumer_secret= 'bghGFrViwWuu8FCcIsEJ1oVVjDmE8ykbLR6nPaNES2w4qX3yor'
access_token= '744048595-zYPiN2KQGsVaxFrp4dv6hJkTYuUHk2M212hI5Q3Y'
access_token_secret= 'eve4jM5eakqdi7nXe0HeKKpsGNEmqtcnX37soBPc4DN9z'

#Keyword
# KC rust
          
#File to store
class listener(StreamListener):
      
    def on_data(self, tweet):
        decoded = json.loads(tweet)

        #print "decoded['text'] " + decoded['text']

        #matchedKeyqords contains the list of commodities symbol matched
        matchedKeywords = findStrings.matchAllKeywords(decoded['text'])


        #filter decoded['text'] and update printNames
        #match against each of commodities.
        #if match is found, run a filter to update printName count
        #There should a filter against each commodity symbol for example
        #if tweet text contains gold, check all printName with commodity gold should be looked for.
        #run a filter for that commodity to search for more keywords to
        #narrow down or update the printName count


        matchedKeywords = ' '.join(matchedKeywords)

        tweetText = decoded['text']
        tweetText = tweetText.lower()

        print decoded['text']

        if 'oil' in tweetText:
            print 'oil'
            filterAndUpdatePrintNameCount(tweetText)

        elif 'gold' in tweetText:
            print 'gold'
            filterAndUpdatePrintNameCount(tweetText)

        elif 'cocoa' in tweetText:
            print 'cocoa'
            filterAndUpdatePrintNameCount(tweetText)

        elif 'copper' in tweetText:
            print 'copper'
            filterAndUpdatePrintNameCount(tweetText)

        elif 'coffee' in tweetText:
            print 'coffee'
            filterAndUpdatePrintNameCount(tweetText)

        elif 'palladium' in tweetText:
            print 'palladium'
            filterAndUpdatePrintNameCount(tweetText)

        elif 'market' in tweetText:
            print 'stockMarket'
            filterAndUpdatePrintNameCount(tweetText)
        else:
            print 'nothing'

        memory.updateKeywordCounts(matchedKeywords)

    def on_error(self, status):
        print status        

# OAuth Authentication using tweepy

auth = twitterAuthentication.getTwitterAuthentication()

#create three streams
twitterStream1 = Stream(auth, listener())
# twitterStream2 = Stream(auth, listener())
# twitterStream3 = Stream(auth, listener())
#twitterStream4 = Stream(auth. listener())



# create a memory object
#Use this only for testing with dummy keywords vaibhav
memory = tweetsKeywordMemory.tweetsKeywordMemory() # this approach seems to be outdated. It just hits the twitter for simple set of keywords
#it does not extend the idea of making a complex query from mixed set of futureTopicsTwitter, marketTopics
#below are few examples of complex structured query
#(oil futures -soybeans) (buy OR long OR buy OR "short covering" -short) (gold futures -jewelry)
#(cocoa futures -drink -cotton -coffee) (buy OR long OR buy OR "short covering" -short) (gold futures -jewelry
#("stock market") (buy OR long OR buy OR "short covering" -short) (gold futures -jewelry)
# These examples covers all sorts of complex structured queries.

#set filter for the stream
#keywordsList = constants.getAllCurrentKeywords()
#collecting only COM TOP TOP type queries
# keywordsList = getAllTwitterKeywords()
# print len(keywordsList)
#print len(keywordsList)
#need to split because 400 maximum
#print keywordsList
keywordsList = ['gold futures', 'palladium futures', 'oil futures', 'stock market', 'coffee futures', 'hogs futures', 'cocoa futures'] #keywordsList[0:300]
#print 'keywordsList1'
#print keywordsList1
#keywordsList1.append('world cup')
# keywordsList2 = keywordsList[300:600] #keywordsList[300:600]
# # print 'keywordsList1'
# #print keywordsList2
# keywordsList3 = keywordsList[600:900] #['oil production' ] #keywordsList[600:800]
# keywordsList4 = keywordsList[900:]

#keywordsList2.append('brasil cup')


# keywordsList1 = '(oil futures -soybeans) (buy OR long OR buy OR "short covering" -short) (gold futures -jewelry) lang:en'
# keywordsList2 = '(cocoa futures -drink -cotton -coffee) (buy OR long OR buy OR "short covering" -short) (gold futures -jewelry) lang:en'







#get Users to follow
#usersID = getTwitterUsers.getTwitterIDs(auth)
#usersID = ['39294671', '290189106', '55020919', '102212196', '26336221', '1467621', '16371383', '330404529', '46633066', '18408663', '18746431', '78925997', '34341067', '2480323728', '146128105', '28349818', '40894124', '97072271', '36992542', '442823943', '512296983', '53073100', '37623257', '22184904', '14673355', '33026200', '24218225', '33488160', '17464780', '172836249', '103925867', '125228250', '57058924', '28361766', '12766862', '101806773', '151180287', '239084885', '323962092', '161153859', '17991579', '25570548', '22120436', '31001654', '17377396', '222625575', '119518329', '85088878', '20274912', '62820756', '38302332', '46759952', '136139641', '89621451', '443828228', '54243900', '45415894', '121902355', '417727024', '20858691', '177239631', '50262721', '270484039', '204187215', '289745762', '21277169', '14609388', '5832212', '5831802', '517189757', '60612630', '301499991', '25448539', '229143589', '28061628', '313644208', '81881292', '195444215', '16672210', '28802292', '541253226', '38328943', '161855898', '124235135', '385658781', '17906329', '24656325', '18370911', '456997996', '21089620', '263611804', '153097154', '94373507', '264643463']


print "Enter 1"
threading.Thread(target=twitterStream1.filter, kwargs={'track': keywordsList}).start()
print "Started 1"
# threading.Thread(target=twitterStream2.filter, kwargs={'track': keywordsList}).start()
# print "Started 2"
# threading.Thread(target=twitterStream3.filter, kwargs={'follow': keywordsList}).start()
#threading.Thread(target=twitterStream3.filter, kwargs={'follow': usersID}).start()
print "Started 3"
#threading.Thread(target=twitterStream4.filter, kwargs={'follow': keywordsList4}).start()
#print "Started users"


#s.filter(follow = userIDs, track = trackWords)
l = listener()
print l
#http://commodityhq.com/2012/100-insightful-futures-traders-worth-following-on-twitter/
#userIDs.append(str(api.get_user(str(status.author.screen_name)).id))
#http://stackoverflow.com/questions/13215054/tweepy-public-stream-filter-by-a-changing-variable
#usersID = ['39294671', '290189106', '55020919', '102212196']



