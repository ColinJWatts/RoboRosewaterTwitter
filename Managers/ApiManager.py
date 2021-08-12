import tweepy

# I swear I thought this was going to need to do more
class ApiManager:

    def __init__(self, api):
        self.api = api

    def SendTweet(self, text):
        self.api.update_status(text)

    def SendImageAsTweet(self, imgFilePath, text):
        self.api.update_with_media(imgFilePath, status=text)