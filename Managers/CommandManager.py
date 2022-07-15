import time
import sys
import os
import threading
from Managers.Logger import Logger

def FindLevenshteinDistance(word1, word2):
    mat = [[0 for j in range(len(word2) + 1)] for i in range(len(word1) + 1)]
    
    for i in range(len(word1) + 1):
        mat[i][0] = i

    for j in range(len(word2) + 1):
        mat[0][j] = j
    
    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            sub = 0
            if word1[i-1] != word2[j-1]:
                sub = 1
            mat[i][j] = min(mat[i-1][j] + 1, mat[i][j-1] + 1, mat[i-1][j-1] + sub)
    return mat[-1][-1]

class CommandManager:

    def __init__(self, config, imageManager, twitterManager, discordManager):
        Logger.LogInfo("Initializing Command Manager")
        self.config = config
        self.imageManager = imageManager
        self.twitterManager = twitterManager
        self.discordManager = discordManager
        self.ConsumeCommandThread = threading.Thread(target=self.ConsumeCommandsTask, daemon=True)
        self.ConsumeCommandThread.start()

    def ConsumeCommandsTask(self):
        Logger.LogInfo("Starting Command Consumer")
        while(True):
            commands = self.discordManager.GetAllCommandsFromQueue()
            for command in commands:
                try:
                    self.DoCommand(command)
                except:
                    Logger.LogError(f"Command failed with exception: {sys.exc_info()}", self.discordManager)

            time.sleep(self.config["CommandCheckFreqSec"])
    
    def DoCommand(self, command):
        query = command.content[len(self.config["CommandPrefix"]):].strip()
        if len(query) > 3 and query[:4] == "sync" and command.author.id in self.config["RestrictedCommandUserWhitelist"]:
            self.SyncImageManager(command)
        # else:
        #     self.GetCardFromSinkCommand(command)

    def SyncImageManager(self, command):
        try:
            self.imageManager.SyncCache()
            self.discordManager.SendMessage(f"Sync Finished", channel=command.channel)
        except:
            self.discordManager.SendMessage(f"Sync Failed with exception: {sys.exc_info()}", channel=command.channel)

    # Ideally this will be a seperate thing but for now I want to try it here
    def GetCardFromSinkCommand(self, command):
        query = command.content[len(self.config["CommandPrefix"]):].strip()
        toGet = query.lower()
        cardInfos = self.imageManager.GetListOfSinkFiles()
        cardInfo = None
        for c in cardInfos:
            if self.imageManager.GetFileNameFromPath(c).lower() == toGet:
                cardInfo = c
                break
        
        if not cardInfo is None: 
            img = self.imageManager.GetFileFromSinkByName(cardInfo)
            path = os.path.join(self.config['DriveImageCachePath'], cardInfo['name'])
            img.save(path)
            self.discordManager.SendMessage(self.imageManager.GetFileNameFromPath(path), imageFilePath=path, channel=command.channel)
            return
        
        # if we get here, we don't have an exact match to a card and must fuzzy match
        lowercaseNames = [self.imageManager.GetFileNameFromPath(c).lower() for c in cardInfos]
        maxLen = len(max(lowercaseNames, key=len))
        paddedNames = [nam.ljust(maxLen, 'A') for nam in lowercaseNames] # note: since all names are now lowercase 'A' is a character no name uses
        distances = []

        minNames = []
        minDist = 100000
        locs = -1

        i = 0
        for name in paddedNames:
            dist = FindLevenshteinDistance(toGet, name)
            if dist < minDist:
                minNames = [self.imageManager.GetFileNameFromPath(cardInfos[i])]
                minDist = dist
                loc = i
            elif dist == minDist:
                minNames.append(self.imageManager.GetFileNameFromPath(cardInfos[i]))
            i+=1

        if len(minNames) == 1:
            path = os.path.join(self.imageManager.sinkCache, cardInfos[loc])
            self.discordManager.SendMessage(f"Could not find card {query}, best match is {minNames[0]}", imageFilePath=path, channel=command.channel)
        else:
            toSend = minNames
            if len(minNames) > self.config["MaxFuzzyMatchResponse"]:
                toSend = minNames[:self.config["MaxFuzzyMatchResponse"]]
            self.discordManager.SendMessage(f"Could not find card {query}, could you mean one of these? {toSend}", channel=command.channel)
