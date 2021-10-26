import datetime
from datetime import timedelta
from datetime import timezone

from Managers.Logger import Logger

class Task:
    # Start Time must be a UTC DateTime (TODO: BUILD UTO TO EST CONVERSION UTILITY)
    # Interval is a timedelta
    # max runs is the total number of times this Task will run
    #   default is set to -1 which means that the task will never stop
    #   0 will never run, 1 will run once, etc
    def __init__(self, startTime, interval, maxRuns=-1):
        Logger.LogInfo(f"{self.__class__.__name__} initially scheduled for {startTime} UTC")
        self.nextRunTime = startTime
        self.interval = interval
        self.maxRuns = maxRuns

    # Incrementing time based on now() could cause the time the task is done to drift
    # incrementing time based on nextRunTime alone could mean we run a task repeatedly if set in the past
    # this function is meant to try to get the best of both worlds
    def IncrementTime(self):
        possibleNextTime = self.nextRunTime + self.interval
        if (possibleNextTime < datetime.datetime.now(timezone.utc)):
            self.nextRunTime = datetime.datetime.now(timezone.utc) + self.interval
        else:
            self.nextRunTime = possibleNextTime
        Logger.LogInfo(f"{self.__class__.__name__} next run scheduled for {self.nextRunTime} UTC")

    # note: tasks may throw
    def Run(self):
        if (self.maxRuns == 0):
            return

        # check if current time is past the next run time
        if (datetime.datetime.now(timezone.utc) > self.nextRunTime):
            Logger.LogInfo(f"Trying to run task: {self.__class__.__name__}")
            self.DoTask() 
            # increment next run time by self.interval
            self.IncrementTime()
            if (self.maxRuns > 0):
                self.maxRuns = self.maxRuns - 1
                Logger.LogInfo(f"{self.__class__.__name__} has {self.maxRuns} more runs")
        
    def DoTask(self):
        print(f"Default task run at time: {datetime.datetime.now(timezone.utc)}")
