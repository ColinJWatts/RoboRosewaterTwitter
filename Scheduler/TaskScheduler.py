import sys
import datetime as dt
import pytz
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import time as t
from Managers.Logger import Logger
from Scheduler.Task import Task
from Scheduler.SendStatusToDiscordTask import SendStatusToDiscordTask 
from Scheduler.TweetRandomImageFromSourceTask import TweetRandomImageFromSourceTask

# note, incoming timezone is assumed to be "America/New_York"
def GetNextOccurenceOfESTTime(time):
    estTimeZone = pytz.timezone("America/New_York")
    testTime = datetime.now()
    testTime = testTime.replace(hour=time.hour, minute=time.minute, second=time.second, microsecond=0)
    testTime = estTimeZone.localize(testTime)
    if testTime > datetime.now(timezone.utc):
        return testTime
    else:
        day = timedelta(days=1)
        return testTime + day

class TaskScheduler:
    def __init__(self, config, twitterManager, imgManager, discordManager):
        Logger.LogInfo("Initializing Task Scheduler")
        self.config = config
        self.twitterManager = twitterManager
        self.imageManager = imgManager
        self.discordManager = discordManager
        self.TaskList = []
        self.LoadDailySchedule()

    def Run(self):
        Logger.LogInfo("Beginning Task Loop")
        while True:
            for task in self.TaskList:
                try:
                    taskResponse = task.Run()
                except:
                    Logger.LogError(f"{task.__class__.__name__} failed with exception: {sys.exc_info()}", self.discordManager)
                    task.IncrementTime() # we make use of the increment function to avoid error spam
                    
            # Pause the thread until we try again
            t.sleep(self.config["TaskTryRunFreqSec"])
    
    def LoadDailySchedule(self):
        dayinterval = timedelta(days=1)

        sendStatusTime = GetNextOccurenceOfESTTime(dt.time(hour=15, minute=0))
        sendStatusTask = SendStatusToDiscordTask(self.config, self.imageManager, self.discordManager, self.twitterManager, sendStatusTime, dayinterval)
        self.TaskList.append(sendStatusTask)

        NineAM = GetNextOccurenceOfESTTime(dt.time(hour=9, minute=0))
        tweetImage9AMTask = TweetRandomImageFromSourceTask(self.config, self.imageManager, self.discordManager, self.twitterManager, NineAM, dayinterval)
        self.TaskList.append(tweetImage9AMTask)

        Noon = GetNextOccurenceOfESTTime(dt.time(hour=12, minute=0))
        tweetImageNoonTask = TweetRandomImageFromSourceTask(self.config, self.imageManager, self.discordManager, self.twitterManager, Noon, dayinterval)
        self.TaskList.append(tweetImageNoonTask)

        SixPM = GetNextOccurenceOfESTTime(dt.time(hour=18, minute=0))
        tweetImage6PMTask = TweetRandomImageFromSourceTask(self.config, self.imageManager, self.discordManager, self.twitterManager, SixPM, dayinterval)
        self.TaskList.append(tweetImage6PMTask)

    def LoadTaskSchedule(self):
        # This is where we load in a schedule
        # Currently, schedule is hardcoded
        estTimeZone = pytz.timezone("America/New_York")
        dayinterval = timedelta(days=1)
        # Example Default Task
        #self.TaskList.append(Task(datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds = 10), datetime.timedelta(seconds = 10), maxRuns=60))
        
        # set up a status reminder task
        sendStatusStartTime = estTimeZone.localize(datetime(2021, 9, 1, hour=10))
        sendStatusTask = SendStatusToDiscordTask(self.imageManager, self.discordManager, self.twitterManager, sendStatusStartTime, dayinterval)
        self.TaskList.append(sendStatusTask)

        # set up a task to tweet images
        NineAM = estTimeZone.localize(datetime(2021, 9, 1, hour=9))
        tweetImage9AMTask = TweetRandomImageFromSourceTask(self.config, self.imageManager, self.discordManager, self.twitterManager, NineAM, dayinterval)
        self.TaskList.append(tweetImage9AMTask)

        Noon = estTimeZone.localize(datetime(2021, 9, 1, hour=12))
        tweetImageNoonTask = TweetRandomImageFromSourceTask(self.config, self.imageManager, self.discordManager, self.twitterManager, Noon, dayinterval)
        self.TaskList.append(tweetImageNoonTask)

        ThreePM = estTimeZone.localize(datetime(2021, 9, 1, hour=15))
        tweetImage3PMTask = TweetRandomImageFromSourceTask(self.config, self.imageManager, self.discordManager, self.twitterManager, ThreePM, dayinterval)
        self.TaskList.append(tweetImage3PMTask)


