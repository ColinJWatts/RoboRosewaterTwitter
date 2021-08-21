import datetime
import sys
from datetime import timezone
import time
from Scheduler.Task import Task
from Scheduler.SendStatusToDiscordTask import SendStatusToDiscordTask 

class TaskScheduler:
    def __init__(self, config, imgManager, discordManager):
        self.config = config
        self.imageManager = imgManager
        self.discordManager = discordManager
        self.TaskList = []

        #self.TaskList.append(Task(datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds = 10), None, maxRuns=60))
        self.TaskList.append(SendStatusToDiscordTask(imgManager, discordManager, datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds = 10), None, maxRuns=60))
    def Run(self):
        while True:
            for task in self.TaskList:
                try:
                    taskResponse = task.Run()
                except:
                    self.discordManager.SendMessage(f"Task failed with exception: {sys.exc_info()[0]}")
            
            # Pause the thread until we try again
            time.sleep(self.config["TaskTryRunFreqSec"])
 