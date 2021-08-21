import tweepy
import json

class TwitterApiManager:

    def __init__(self, config):
        self.config = config
        secretFile = open(self.config["TwitterSecretsPath"], "r")
        secrets = json.loads(secretFile.read())

        auth = tweepy.OAuthHandler(secrets["CONSUMER_KEY"], secrets["CONSUMER_SECRET"])
        auth.set_access_token(secrets["ACCESS_KEY"], secrets["ACCESS_SECRET"])
        self.api = tweepy.API(auth)

    def SendTweet(self, text):
        self.api.update_status(text)

    def SendImageAsTweet(self, imgFilePath, text):
        self.api.update_with_media(imgFilePath, status=text)