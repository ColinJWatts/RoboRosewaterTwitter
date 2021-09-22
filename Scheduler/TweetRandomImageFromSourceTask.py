import sys
import time
import threading
from Scheduler.Task import Task
from Managers.Logger import Logger

twitterLock = threading.Lock()
def ReleaseLockAfterMinute():
    time.sleep(60)
    twitterLock.release()

class TweetRandomImageFromSourceTask(Task): 
    def __init__(self, config, imageManager, discordManager, twitterManager, startTime, interval, maxRuns=-1, ExtraTweetText=""): 
        super().__init__(startTime, interval, maxRuns)
        self.config = config
        self.imageManager = imageManager
        self.discordManager = discordManager
        self.twitterManager = twitterManager
        self.extraTweetText = ExtraTweetText

    def DoTask(self):
        if twitterLock.acquire(blocking=False):
            releaseTask = threading.Thread(target=ReleaseLockAfterMinute, daemon=True)
            releaseTask.start()
            localFilePath = self.imageManager.DownloadAndMoveRandomImage()
            if (localFilePath is None):
                Logger.LogWarning("Tried to send tweet but could not find an image", self.discordManager)
                return

            fileName = self.imageManager.GetFileNameFromPath(localFilePath)

            try:
                status = self.twitterManager.SendImageAsTweet(localFilePath, f"{fileName} {self.extraTweetText}")
                Logger.LogInfo(f"New card tweeted: {fileName}")
                url = self.config["TwitterStatusBaseUrl"] + str(status.id)# f{status.id}"

                self.discordManager.SendMessage(f"New card tweeted: {fileName}\n{url}")
            except:
                Logger.LogError(f"Failed to send tweet for card: {fileName}\n  Failed with exception: {sys.exc_info()}", self.discordManager)
        else: 
            Logger.LogInfo("Twitter task blocked from sending tweet")