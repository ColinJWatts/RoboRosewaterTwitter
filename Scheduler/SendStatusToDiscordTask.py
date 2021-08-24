from Scheduler.Task import Task

class SendStatusToDiscordTask(Task):
    def __init__(self, imageManager, discordManager, twitterManager, startTime, interval, maxRuns=-1):
        super().__init__(startTime, interval, maxRuns)
        self.imageManager = imageManager
        self.discordManager = discordManager
        self.twitterManager = twitterManager

    def DoTask(self):
        message = ""
        imgInfos = self.imageManager.GetListOfAllImageInfo()
        message += f"Number of images queued for tweeting: {len(imgInfos)}\n"

        numFollowers = self.twitterManager.GetNumberOfFollowers()
        message += f"Number of followers on Twitter: {numFollowers}\n"

        self.discordManager.SendMessage(message)