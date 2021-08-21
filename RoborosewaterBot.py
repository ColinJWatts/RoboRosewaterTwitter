import json
from Managers.ApiManager import ApiManager
from Managers.DriveImageManager import DriveImageManager
from Managers.DiscordManager import DiscordManager
from Scheduler.TaskScheduler import TaskScheduler

class RoborosewaterBot:

    def __init__(self, api, configPath):
        self.config = json.loads(open(configPath, 'r').read())
        self.discordManager = DiscordManager(self.config)
        self.api = ApiManager(api)
        self.imageManager = DriveImageManager(self.config)
        self.scheduler = TaskScheduler(self.config, self.imageManager, self.discordManager)
        
        
    def Start(self):
        self.scheduler.Run()
        #self.SendRandomImageFromSource()

    def SendRandomImageFromSource(self):
        print(self.imageManager.DownloadAndMoveRandomImage())
