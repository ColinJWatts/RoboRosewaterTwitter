import sys
import time
import threading
from Scheduler.Task import Task
from Managers.Logger import Logger
from Managers.TwitterApiManager import twitterLock


class TweetRandomImageFromSourceTask(Task): 
    def __init__(self, config, imageManager, discordManager, twitterManager, startTime, interval, maxRuns=-1, ExtraTweetText=""): 
        super().__init__(startTime, interval, maxRuns)
        self.config = config
        self.imageManager = imageManager
        self.discordManager = discordManager
        self.twitterManager = twitterManager
        self.extraTweetText = ExtraTweetText

    def DoTask(self):
        if not twitterLock.locked():
            localFilePath = self.imageManager.GetRandomImageFilePath()
            if (localFilePath is None):
                Logger.LogWarning("Tried to send tweet but could not find an image", self.discordManager)
                return

            fileName = self.imageManager.GetFileNameFromPath(localFilePath)

            try:
                textReply = self.imageManager.TryGetTextForImage(fileName)
                altText = ""
                if not textReply is None:
                    if len(textReply) >= 1000:
                        textReply = textReply[:999]
                    altText = textReply
                status = self.twitterManager.SendImageAsTweet(localFilePath, f"{fileName} {self.extraTweetText}", altText=altText)
                
                if status is None:
                    Logger.LogWarning(f"Failed to send image [{fileName}] due to rate limit", self.discordManager)
                    return 
                
                Logger.LogInfo(f"New card tweeted: {fileName}")
                
                url = self.config["TwitterStatusBaseUrl"] + str(status.id)
                
                newPath = self.imageManager.MoveImageToSink(localFilePath)
                tweetChannel = self.discordManager.GetTweetChannel()

                path = None
                if self.config["SuppressEmbed"]:
                    # if we're suppressing the link embeddings in twitter we want to send the image to discord too
                    path = newPath
                    url = f"<{url}>"

                if not tweetChannel is None:
                    self.discordManager.SendMessage(f"New card tweeted: {fileName}\n{url}", imageFilePath=path, channel=tweetChannel)
                else: 
                    self.discordManager.SendMessage(f"New card tweeted: {fileName}\n{url}", imageFilePath=path)

            except:
                Logger.LogError(f"Failed to send tweet for card: {fileName}\n  Failed with exception: {sys.exc_info()}", self.discordManager)
        else: 
            Logger.LogInfo("Twitter has already been locked, bailing on task")