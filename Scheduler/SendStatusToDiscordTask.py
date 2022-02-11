from Scheduler.Task import Task

class SendStatusToDiscordTask(Task):
    def __init__(self, config, imageManager, discordManager, twitterManager, startTime, interval, maxRuns=-1):
        super().__init__(startTime, interval, maxRuns)
        self.config = config
        self.imageManager = imageManager
        self.discordManager = discordManager
        self.twitterManager = twitterManager

    def DoTask(self):
        message = ""
        imgInfos = self.imageManager.GetListOfSourceFiles()
        message += f"Number of images queued for tweeting: {len(imgInfos)}\n"

        if self.config["PriorityDriveFolder"] != "":
            numPriority = len(self.imageManager.GetListOfPriorityFiles())
            if numPriority > 0:
                message += f"Number of images in priority queue: {numPriority}\n"

        numFollowers = self.twitterManager.GetNumberOfFollowers()
        message += f"Number of followers on Twitter: {numFollowers}\n"

        numTweets = self.twitterManager.GetNumberOfTweets()
        message += f"Total number of tweets: {numTweets}\n"

        self.discordManager.SendMessage(message)