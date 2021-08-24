from Scheduler.Task import Task

class TweetRandomImageFromSourceTask(Task): 
    def __init__(self, imageManager, discordManager, twitterManager, startTime, interval, maxRuns=-1): 
        super().__init__(startTime, interval, maxRuns)

        self.imageManager = imageManager
        self.discordManager = discordManager
        self.twitterManager = twitterManager

    def DoTask(self):
        localFilePath = self.imageManager.DownloadAndMoveRandomImage()
        if (localFilePath is None):
            self.discordManager.SendMessage("Tried to send tweet but could not find an image")
            return
            
        fileName = self.imageManager.GetFileNameFromPath(localFilePath)
        
        try:
            self.twitterManager.SendImageAsTweet(localFilePath, fileName)
            self.discordManager.SendMessage(f"New card tweeted: {fileName}", localFilePath)
        except:
            self.discordManager.SendMessage(f"Failed to send tweet for card: {fileName}")