from Scheduler.Task import Task
from Managers.Logger import Logger

class TweetRandomImageFromSourceTask(Task): 
    def __init__(self, imageManager, discordManager, twitterManager, startTime, interval, maxRuns=-1): 
        super().__init__(startTime, interval, maxRuns)

        self.imageManager = imageManager
        self.discordManager = discordManager
        self.twitterManager = twitterManager

    def DoTask(self):
        localFilePath = self.imageManager.DownloadAndMoveRandomImage()
        if (localFilePath is None):
            Logger.LogWarning("Tried to send tweet but could not find an image", self.discordManager)
            return
            
        fileName = self.imageManager.GetFileNameFromPath(localFilePath)
        
        try:
            self.twitterManager.SendImageAsTweet(localFilePath, fileName)
            Logger.LogInfo(f"New card tweeted: {fileName}")
            self.discordManager.SendMessage(f"New card tweeted: {fileName}", localFilePath)
        except:
            Logger.LogError(f"Failed to send tweet for card: {fileName}\n  Failed with exception: {sys.exc_info()}", self.discordManager)
