import json
import tweepy
import findStrings
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#keys for Authentication
consumer_key= 'ytwg4fSktfnqbktUIkhlaWggQ'
consumer_secret= 'bghGFrViwWuu8FCcIsEJ1oVVjDmE8ykbLR6nPaNES2w4qX3yor'
access_token= '744048595-zYPiN2KQGsVaxFrp4dv6hJkTYuUHk2M212hI5Q3Y'
access_token_secret= 'eve4jM5eakqdi7nXe0HeKKpsGNEmqtcnX37soBPc4DN9z'

#Keyword
# KC rust
keywords = ['brazil frost', 'brazil storm crops', 'brazil weather markets', 'Brazilian Real price', 'coffee Arabica ', \
            'coffee brazil crop', 'coffee columbia', 'coffee crop', 'coffee demand', 'coffee downside', \
            'coffee export', 'coffee exports', 'coffee forecast', 'coffee freeze', 'coffee frost', \
            'coffee futures', 'coffee harvest', 'coffee imports', 'coffee indonesia', 'coffee outlook', \
            'coffee production', 'coffee rally', 'coffee risk', 'coffee shortage', 'coffee surplus', \
            'coffee vietnam', 'coffee profits', 'coffee supply', 'coffee price upside',  \
            'coffee price downside', 'coffee market', 'coffee bullish', 'coffee bearish', 'coffee sector', \
            'coffee acres', 'trading coffee', 'coffee beans market', 'coffee contract', 'coffee drought', \
            'coffee prices down', 'coffee prices up', 'fungus coffee']

#File to store
count = 0
file='tweets.txt'

class listener(StreamListener):
    def on_data(self, data):
        tweet=data
        decoded = json.loads(tweet)
        print decoded['text']
        print findStrings.match_keywords(decoded['text'], keywords)
        print '\n'
        f = open(file,'a')
        try:
            f.write(str(decoded['text']))
            f.write('/n')
        except:
            f.close()
        return True

    def on_error(self, status):
        print status

# OAuth Authentication uing tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#create a stream
twitterStream = Stream(auth, listener())

#set filter for the stream
twitterStream.filter(track=keywords)

