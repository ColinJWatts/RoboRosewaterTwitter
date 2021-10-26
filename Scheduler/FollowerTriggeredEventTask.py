from Scheduler.Task import Task
import datetime
from datetime import timezone
from datetime import timedelta

from Managers.Logger import Logger

class FollowerTriggeredEventTask(Task):
    def __init__(self, imageManager, discordManager, twitterManager, interval, maxRuns, followerThreshold, initialTweetText=None, additionalTweetText=None):
        self.imageManager = imageManager
        self.discordManager = discordManager
        self.twitterManager = twitterManager

        self.followerThreshold = followerThreshold
        self.initialTweetText = initialTweetText
        self.additionalTweetText = additionalTweetText

        startTime = datetime.datetime.now(timezone.utc) + timedelta(hours=1)
        startTime.minute = 0
        startTime.second = 0
        startTime.microsecond = 0
        print(startTime)
        
        self.taskTriggered = False
        super().__init__(startTime, interval, maxRuns=maxRuns)
    
    def Run(self):
        if (self.maxRuns == 0):
            return

        # check if current time is past the next run time
        if (datetime.datetime.now(timezone.utc) > self.nextRunTime):
            numFollowers = self.twitterManager.GetNumberOfFollowers()
            if numFollowers >= self.followerThreshold or self.taskTriggered:
                if self.taskTriggered == False:
                    Logger.LogWarning(f"{self.followerThreshold} follower event has been triggered.", self.discordManager)
                self.taskTriggered = True
                Logger.LogInfo(f"Trying to run task: {self.__class__.__name__}")
                self.DoTask() 
                if (self.maxRuns > 0):
                    self.maxRuns = self.maxRuns - 1
                    Logger.LogInfo(f"{self.__class__.__name__} has {self.maxRuns} more runs")
            # increment next run time by self.interval
            self.IncrementTime()
            
    def DoTask(self):
        numFollowers = self.twitterManager.GetNumberOfFollowers()
        if numFollowers >= self.followerThreshold or self.taskTriggered:
            
            #do task things
            i = 0
        else:
            self.maxRuns += 1
