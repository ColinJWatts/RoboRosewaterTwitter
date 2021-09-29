import json
from Managers.TwitterApiManager import TwitterApiManager
from Managers.DriveImageManager import DriveImageManager
from Managers.DiscordManager import DiscordManager
from Managers.CommandManager import CommandManager
from Scheduler.TaskScheduler import TaskScheduler
from Managers.Logger import Logger

class RoborosewaterBot:

    def __init__(self, configPath):
        Logger.LogInfo("Initializing Bot")
        self.config = json.loads(open(configPath, 'r').read())
        self.discordManager = DiscordManager(self.config)
        self.twitterManager = TwitterApiManager(self.config)
        self.imageManager = DriveImageManager(self.config)
        self.scheduler = TaskScheduler(self.config, self.twitterManager, self.imageManager, self.discordManager)
        self.CommandManager = CommandManager(self.config, self.imageManager, self.twitterManager, self.discordManager)

    def Start(self):
        Logger.LogInfo("Starting Bot")
        self.scheduler.Run()
