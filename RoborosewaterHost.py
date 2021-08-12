import json
import tweepy
from RoborosewaterBot import RoborosewaterBot

# Read secrets
secretFile = open("./secrets.txt", "r")
secrets = json.loads(secretFile.read())

# Do authentication
auth = tweepy.OAuthHandler(secrets["CONSUMER_KEY"], secrets["CONSUMER_SECRET"])
auth.set_access_token(secrets["ACCESS_KEY"], secrets["ACCESS_SECRET"])
api = tweepy.API(auth)

bot = RoborosewaterBot(api, "./config.json")

bot.Start()