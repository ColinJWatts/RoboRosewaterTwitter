import sys
import datetime
import pytz
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import time
from Scheduler.Task import Task
from Scheduler.SendStatusToDiscordTask import SendStatusToDiscordTask 
from Scheduler.TweetRandomImageFromSourceTask import TweetRandomImageFromSourceTask

class TaskScheduler:
    def __init__(self, config, twitterManager, imgManager, discordManager):
        self.config = config
        self.twitterManager = twitterManager
        self.imageManager = imgManager
        self.discordManager = discordManager
        self.TaskList = []
        self.LoadTaskSchedule()

    def Run(self):
        while True:
            for task in self.TaskList:
                try:
                    taskResponse = task.Run()
                except:
                    self.discordManager.SendMessage(f"Task failed with exception: {sys.exc_info()[0]}")
                    task.IncrementTime() # we make use of the increment function to avoid error spam
                    
            # Pause the thread until we try again
            time.sleep(self.config["TaskTryRunFreqSec"])
    

    def LoadTaskSchedule(self):
        # This is where we load in a schedule
        # Currently, schedule is hardcoded

        # Example Default Task
        #self.TaskList.append(Task(datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds = 10), datetime.timedelta(seconds = 10), maxRuns=60))
        
        # set up a status reminder task
        sendStatusStartTime = self.ESTtoUTC(datetime(2021, 8, 24, hour=8, minute=30))
        sendStatusInterval = timedelta(minutes=180)
        sendStatusTask = SendStatusToDiscordTask(self.imageManager, self.discordManager, self.twitterManager, sendStatusStartTime, sendStatusInterval)
        self.TaskList.append(sendStatusTask)

        # set up a task to tweet images
        tweetImageStartTime = self.ESTtoUTC(datetime(2021, 8, 24, hour=8, minute=30))
        tweetImageInterval = timedelta(minutes=30)
        tweetImageTask = TweetRandomImageFromSourceTask(self.imageManager, self.discordManager, self.twitterManager, tweetImageStartTime, tweetImageInterval)
        self.TaskList.append(tweetImageTask)

    def ESTtoUTC(self, estTime):
        utcTime = estTime + timedelta(hours = -self.config["EasterStandardTimeOffset"])
        return utcTime.replace(tzinfo=pytz.UTC)
    def UTCtoEST(self, utcTime):
        return utcTime + timedelta(hours = self.config["EasterStandardTimeOffset"])
