import json
from Managers.TwitterApiManager import TwitterApiManager
from Managers.DriveImageManager import DriveImageManager
from Managers.DiscordManager import DiscordManager
from Scheduler.TaskScheduler import TaskScheduler

class RoborosewaterBot:

    def __init__(self, configPath):
        self.config = json.loads(open(configPath, 'r').read())
        self.discordManager = DiscordManager(self.config)
        self.twitterManager = TwitterApiManager(self.config)
        self.imageManager = DriveImageManager(self.config)
        self.scheduler = TaskScheduler(self.config, self.twitterManager, self.imageManager, self.discordManager)
        
        
    def Start(self):
        self.scheduler.Run()
        #self.SendRandomImageFromSource()

    def SendRandomImageFromSource(self):
        print(self.imageManager.DownloadAndMoveRandomImage())
