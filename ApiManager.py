import tweepy

def class ApiManager:

    def __init__(self, api):
        self.api = api

    def SendTweet(self, text):
        api.update_status('Updating using OAuth authentication via Tweepy!')

    def SendImageAsTweet(self, imgFilePath):
        filename = "get image file name"
        self.SendImageAsTweet(imgFilePath, filename)

    def SendImageAsTweet(self, imgFilePath, text):
        return