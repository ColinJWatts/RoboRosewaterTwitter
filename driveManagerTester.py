from Managers.CachedDriveImageManager import CachedDriveImageManager
from Managers.DiscordManager import DiscordManager
from Managers.TwitterApiManager import TwitterApiManager
from Scheduler.TweetRandomImageFromSourceTask import TweetRandomImageFromSourceTask
from Scheduler.SendStatusToDiscordTask import SendStatusToDiscordTask
from Scheduler.SyncCacheTask import SyncCacheTask
import json
import time

config = json.loads(open(".//config.json", 'r').read())
imageManager = CachedDriveImageManager(config)
discordManager = DiscordManager(config)
twitterManager = TwitterApiManager(config)

task = TweetRandomImageFromSourceTask(config, imageManager, discordManager, twitterManager, None, None)
status = SendStatusToDiscordTask(config, imageManager, discordManager, twitterManager, None, None)

input()

task.DoTask()
time.sleep(2)
status.DoTask()
time.sleep(2)
#print(len(manager.GetListOfAllImageInfo()))
#manager.PrintTokenInfo()
#manager.RefreshCredentials()
#print(len(manager.GetListOfAllImageInfo()))
#manager.PrintTokenInfo()