#get twitter authorization once!
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy

#keys for Authentication
consumer_key= 'ytwg4fSktfnqbktUIkhlaWggQ'
consumer_secret= 'bghGFrViwWuu8FCcIsEJ1oVVjDmE8ykbLR6nPaNES2w4qX3yor'
access_token= '744048595-zYPiN2KQGsVaxFrp4dv6hJkTYuUHk2M212hI5Q3Y'
access_token_secret= 'eve4jM5eakqdi7nXe0HeKKpsGNEmqtcnX37soBPc4DN9z'

# OAuth Authentication using tweepy
def getTwitterAuthorization():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

#Working Fine when tested
# auth = getTwitterAuthorization()
# print auth.access_token
# print auth.access_token_secret
# print auth.consumer_key
# print auth.consumer_secret
