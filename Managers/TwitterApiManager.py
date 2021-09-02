import tweepy
import json
from Managers.Logger import Logger

class TwitterApiManager:

    def __init__(self, config):
        self.config = config
        Logger.LogInfo("Starting Twitter Manager")
        secretFile = open(self.config["TwitterSecretsPath"], "r")
        secrets = json.loads(secretFile.read())

        auth = tweepy.OAuthHandler(secrets["CONSUMER_KEY"], secrets["CONSUMER_SECRET"])
        auth.set_access_token(secrets["ACCESS_KEY"], secrets["ACCESS_SECRET"])
        self.api = tweepy.API(auth)

    def SendTweet(self, text):
        Logger.LogInfo(f"Sending tweet with text: {text}")
        self.api.update_status(text)

    def SendImageAsTweet(self, imgFilePath, text):
        Logger.LogInfo(f"Tweeting an image with text {text}")
        media = self.api.media_upload(imgFilePath)
        self.api.update_status(status=text, media_ids=[media.media_id])

    def GetNumberOfFollowers(self):
        myInfo = self.api.me()
        return myInfo.followers_count