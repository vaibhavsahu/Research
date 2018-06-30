#get twitter twitterAuthentication once!
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#keys for Authentication
consumer_key= 'ytwg4fSktfnqbktUIkhlaWggQ'
consumer_secret= 'bghGFrViwWuu8FCcIsEJ1oVVjDmE8ykbLR6nPaNES2w4qX3yor'
access_token= '744048595-zYPiN2KQGsVaxFrp4dv6hJkTYuUHk2M212hI5Q3Y'
access_token_secret= 'eve4jM5eakqdi7nXe0HeKKpsGNEmqtcnX37soBPc4DN9z'

# OAuth Authentication uing tweepy
def getTwitterAuthentication():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth
