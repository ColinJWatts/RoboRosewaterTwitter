from Scheduler.Task import Task

class SendStatusToDiscordTask(Task):
    def __init__(self, imageManager, discordManager, startTime, interval, maxRuns=-1):
        super().__init__(startTime, interval, maxRuns)
        self.imageManager = imageManager
        self.discordManager = discordManager

    def DoTask(self):
        imgInfos = self.imageManager.GetListOfAllImageInfo()
        self.discordManager.SendMessage(f"There are currently {len(imgInfos)} images queued")