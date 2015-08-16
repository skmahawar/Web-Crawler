#!/usr/bin/env python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from mongoengine import *
import json
from pprint import pprint

# consumer key, consumer secret, access token, access secret.
TWITTER_APP_KEY = 'eU1CMGuAarU2jO078iuOm0W6O'
TWITTER_APP_KEY_SECRET = 'nFKvstOzMaOMAAMOwluikfQJFRMmOjNxHmOQOI0aCOQg0p1Zlu'
TWITTER_ACCESS_TOKEN = '3069167335-HCixZgPmk35bBBPq3MOvpNX6xaflC7SLkwy3Tj3'
TWITTER_ACCESS_TOKEN_SECRET = 'ND7Xwqkdr9OqUUiCoRyW7J3QqIY8SbhY94goNCmjKW8eF'

#keys = ["Mobiles", "Samsung", "Apple", "IPhone", "HTC", "Micromax", "Motorola", "Microsoft", "Nokia"]

connect('twitter_db')
class Page(Document):
    tweet = DictField()

with open ("data.docx", "r") as myfile:
    keys=myfile.readlines()
k = 0
for word in keys:
    keys[k] = word[0:-1]
    k += 1

print(keys)

class listener(StreamListener):
    def __init__(self, api=None):
        super(listener, self).__init__()
        self.num_tweets = 0

    def on_data(self, data):

        try:
            self.num_tweets += 1
            if self.num_tweets < 10000:
                all_data = json.loads(data)
                print(str(all_data["user"]["screen_name"]) + " :" + str(all_data["user"]["followers_count"]))
                print(all_data["text"])
                print(all_data["retweet_count"])
                Page(tweet=all_data).save()
                return True
            else:
                return (False)
        except:
            self.num_tweets += 1

    def on_error(self, status):
        print status

    def on_timeout(self, status):
        print 'Stream disconnected; continuing...'


auth = OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

for key in keys:
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=[key])
