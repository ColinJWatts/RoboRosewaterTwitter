from Scheduler.Task import Task
from datetime import timedelta

class SyncCacheTask(Task):
    def __init__(self, imageManager, startTime, interval=timedelta(days=1), maxRuns=-1):
        super().__init__(startTime, interval, maxRuns)
        self.enabled = False

        if type(imageManager).__name__ == "CachedDriveImageManager":
            self.enabled = True

        self.imageManager = imageManager

    def DoTask(self):
        if self.enabled:
            self.imageManager.SyncCache()