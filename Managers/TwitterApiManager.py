import tweepy
import json
from Managers.Logger import Logger
import threading
import time

twitterLock = threading.Lock()
def ReleaseLockAfterMinute():
    time.sleep(60)
    twitterLock.release()

class TwitterApiManager:

    def __init__(self, config):
        self.config = config
        Logger.LogInfo("Starting Twitter Manager")
        secretFile = open(self.config["TwitterSecretsPath"], "r")
        secrets = json.loads(secretFile.read())

        auth = tweepy.OAuthHandler(secrets["CONSUMER_KEY"], secrets["CONSUMER_SECRET"])
        auth.set_access_token(secrets["ACCESS_KEY"], secrets["ACCESS_SECRET"])
        self.api = tweepy.API(auth)
    

    # If blocking is true, this call will wait until the lock is released and then take the lock and send the tweet
    # If blocking is false, it will return False if the lock has been taken and fail to send the tweet
    def SendTweet(self, text, blocking=False):
        if twitterLock.acquire(blocking):
            releaseTask = threading.Thread(target=ReleaseLockAfterMinute, daemon=True)
            releaseTask.start()
            Logger.LogInfo(f"Sending tweet with text: {text}")
            return self.api.update_status(text)
        else:
            Logger.LogInfo("Tweet Blocked by timeout ")
            return None

    def TweetIgnoreRateLimit(self, text):
        Logger.LogInfo(f"Sending tweet with text, ignoring lock: {text}")
        return self.api.update_status(text)

    def SendImageAsTweet(self, imgFilePath, text, altText="", blocking=False):
        if twitterLock.acquire(blocking):
            releaseTask = threading.Thread(target=ReleaseLockAfterMinute, daemon=True)
            releaseTask.start()
            Logger.LogInfo(f"Tweeting an image with text {text}")
            media = self.api.media_upload(imgFilePath)
            if altText != "":
                self.api.create_media_metadata(media.media_id, altText)
            return self.api.update_status(status=text, media_ids=[media.media_id])
        else:
            Logger.LogInfo("Tweet Blocked by timeout ")
            return None

    def ReplyToTweet(self, text, tweetIdToReplyTo):
        Logger.LogInfo(f"Replying to tweet with id {tweetIdToReplyTo}")
        return self.api.update_status(status=text, in_reply_to_status_id=tweetIdToReplyTo, auto_populate_reply_metadata=True)

    def GetNumberOfFollowers(self):
        myInfo = self.api.me()
        return myInfo.followers_count
    
    def GetNumberOfTweets(self):
        myInfo = self.api.me()
        return myInfo.statuses_count 