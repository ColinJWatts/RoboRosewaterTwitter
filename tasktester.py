import json
import time

from Managers.TwitterApiManager import TwitterApiManager
from Managers.DriveImageManager import DriveImageManager
from Managers.DiscordManager import DiscordManager

from Scheduler.TweetRandomImageFromSourceTask import TweetRandomImageFromSourceTask
config = json.loads(open("./config.json", 'r').read())
twitterManager = TwitterApiManager(config)
discordManager = DiscordManager(config)
imageManager = DriveImageManager(config, discordManager)

task = TweetRandomImageFromSourceTask(config, imageManager, discordManager, twitterManager, None, None)
task2 = TweetRandomImageFromSourceTask(config, imageManager, discordManager, twitterManager, None, None)
x = ""
while x != "go":
    x = input()
task.DoTask()
task2.DoTask()
time.sleep(60)
task2.DoTask()
task.DoTask()