from Managers.DriveImageManager import DriveImageManager
from Managers.Logger import Logger
from PIL import Image
import random
import time
import os

ACTION_LOG = "ActionLog.txt"

class CachedDriveImageManager:
    def __init__(self, config):
        self.config = config
        Logger.LogInfo("Initiallizing Cached DriveManager")
        self.driveManager = DriveImageManager(config)

        # Set up local cache/make sure it exsists
        self.sourceCache = os.path.join(config["DriveImageCachePath"], "Source")
        self.sinkCache = os.path.join(config["DriveImageCachePath"], "Sink")
        self.priorityCache = os.path.join(config["DriveImageCachePath"], "Priority")
        self.textCache = os.path.join(config["DriveImageCachePath"], "Text")

        if not os.path.isdir(self.sourceCache):
            os.makedirs(self.sourceCache)
        if not os.path.isdir(self.sinkCache):
            os.makedirs(self.sinkCache)
        if not os.path.isdir(self.priorityCache):
            os.makedirs(self.priorityCache)
        if not os.path.isdir(self.textCache):
            os.makedirs(self.textCache)

        self.SyncCache()

    def SyncCache(self):
        Logger.LogInfo("Attempting to sync local cache with Drive")
        # load data we'll need into memory
        # we do this first so that if drive credentials fail this method will fail fast
        sourceDriveInfo = self.driveManager.GetListOfAllImageInfo(self.config["SourceDriveFolder"])
        cachedSourceFileList = [x for x in os.listdir(self.sourceCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]
        
        priorityDriveInfo = self.driveManager.GetListOfAllImageInfo(self.config["PriorityDriveFolder"])
        cachedPriorityFileList = [x for x in os.listdir(self.priorityCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]

        cachedSinkFileList = [x for x in os.listdir(self.sinkCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]

        # Identify local actions taken on the cache and replicate them on drive
        if os.path.isfile(ACTION_LOG):
            f = open(ACTION_LOG, 'r')
            actions = f.readlines()
            for action in actions:
                folderChar = action[0]
                imageFileName = action[1:].strip()

                if folderChar == 'P':
                    driveInfo = priorityDriveInfo
                elif folderChar == 'S':
                    driveInfo = sourceDriveInfo
                else:
                    raise Exception("Drive Sync Failed. Action log was invalid")

                for info in driveInfo:
                    if info['name'] == imageFileName:
                        #remove this image from drive and reupload from cached sink (if able)
                        self.driveManager.RemoveImageById(info['id'])
                        if imageFileName in cachedSinkFileList:
                            self.driveManager.UploadImageToFolder(os.path.join(self.sinkCache, imageFileName), self.config["SinkDriveFolder"])
            
            f.close()
            os.remove(ACTION_LOG)
        
        # refresh these down here because they may have changed
        sourceDriveInfo = self.driveManager.GetListOfAllImageInfo(self.config["SourceDriveFolder"])
        priorityDriveInfo = self.driveManager.GetListOfAllImageInfo(self.config["PriorityDriveFolder"])
        sinkDriveInfo = self.driveManager.GetListOfAllImageInfo(self.config["SinkDriveFolder"])

        # also snag these
        textDriveInfo = self.driveManager.GetListOfAllImageInfo(self.config["TextDescriptionDriveFolder"])
        cachedTextFileList = [x for x in os.listdir(self.textCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]

        # Then find anything that exists in the drive and not locally and download
        for imageInfo in sourceDriveInfo:
            try:
                if not imageInfo['name'] in cachedSourceFileList:
                    img = self.driveManager.DownloadCardById(imageInfo['id'])
                    path = os.path.join(self.sourceCache, imageInfo['name'])
                    img.save(path)
                    time.sleep(.05) # doing this to rate limit downloads to 20/second max
            except: 
                Logger.LogWarning(f"Downloading image ({imageInfo['name']}) from source failed")
     
        for imageInfo in priorityDriveInfo:
            try:
                if not imageInfo['name'] in cachedPriorityFileList:
                    img = self.driveManager.DownloadCardById(imageInfo['id'])
                    path = os.path.join(self.priorityCache, imageInfo['name'])
                    img.save(path)
                    time.sleep(.05)
            except: 
                Logger.LogWarning(f"Downloading image ({imageInfo['name']}) from priority failed")
     
        for imageInfo in sinkDriveInfo:
            try: 
                if not imageInfo['name'] in cachedSinkFileList:
                    img = self.driveManager.DownloadCardById(imageInfo['id'])
                    path = os.path.join(self.sinkCache, imageInfo['name'])
                    img.save(path)
                    time.sleep(.05)
            except:
                Logger.LogWarning(f"Downloading image ({imageInfo['name']}) from sink failed")
        
        for fileInfo in textDriveInfo:
            try:
                if not fileInfo['name'] in cachedTextFileList:
                    path = os.path.join(self.textCache, fileInfo['name'])
                    self.driveManager.DownloadTextFileById(fileInfo['id'], path)
                    time.sleep(.05)
            except:
                Logger.LogWarning(f"Downloading text file ({fileInfo['name']}) failed")

        # Finally, remove any files from the local cache that are not in drive 
        toRemove = [] # we use this to ease logging

        driveSourceFileNames = [x['name'] for x in sourceDriveInfo]
        for fileName in cachedSourceFileList:
            if not fileName in driveSourceFileNames:
                toRemove.append(os.path.join(self.sourceCache, fileName))

        drivePriorityFileNames = [x['name'] for x in priorityDriveInfo]
        for fileName in cachedPriorityFileList:
            if not fileName in drivePriorityFileNames:
                toRemove.append(os.path.join(self.priorityCache, fileName))

        driveSinkFileNames = [x['name'] for x in sinkDriveInfo]
        for fileName in cachedSinkFileList:
            if not fileName in driveSinkFileNames:
                toRemove.append(os.path.join(self.sinkCache, fileName))

        driveTextFileNames = [x['name'] for x in textDriveInfo]
        for fileName in cachedTextFileList:
            if not fileName in driveTextFileNames:
                toRemove.append(os.path.join(self.textCache, fileName))

        for filePath in toRemove:
            Logger.LogInfo(f"Removing card from local cache: {self.driveManager.GetFileNameFromPath(filePath)}")
            os.remove(filePath)

        return

    def TryGetTextForImage(self, imageName):
        textFiles = self.GetListOfTextFiles()
        for text in textFiles:
            if self.GetFileNameFromPath(text) == self.GetFileNameFromPath(imageName):
                return open(os.path.join(self.textCache, text), 'r').read()
        return None
    
    def GetListOfSourceFiles(self):
        return [x for x in os.listdir(self.sourceCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]

    def GetListOfPriorityFiles(self):
        return [x for x in os.listdir(self.priorityCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]

    def GetListOfSinkFiles(self):
        return [x for x in os.listdir(self.sinkCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]

    def GetListOfTextFiles(self):
        return [x for x in os.listdir(self.textCache) if ".txt" in x]

    def GetFileNameFromPath(self, path):
        return self.driveManager.GetFileNameFromPath(path)

    def GetFileFromSinkByName(self, fileName):
        sinkFiles = self.GetListOfSinkFiles()
        if not fileName in sinkFiles:
            return None
        
        return Image.open(os.path.join(self.sinkCache, fileName))

    def GetAndMoveRandomImage(self):
        # We ONLY move this locally
        cachedPriorityFileList = [x for x in os.listdir(self.priorityCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]
        cachedSourceFileList = [x for x in os.listdir(self.sourceCache) if any(filetype in x for filetype in self.config["SupportedFileTypes"])]

        # try to pull from priority first
        if len(cachedPriorityFileList) > 0:
            r = random.randrange(0, len(cachedPriorityFileList))
            imgName = cachedPriorityFileList[r]
            imgPath = os.path.join(self.priorityCache, imgName)
            result = os.path.join(self.sinkCache, imgName)
            Logger.LogInfo(f"Moving image from Priority Cache to Sink Cache: {self.driveManager.GetFileNameFromPath(imgName)}")
            f = open(ACTION_LOG, 'a')
            f.write(f"P{imgName}\n")
            f.close()
            os.replace(imgPath, result)
            return result
            
        # then from regular source
        if len(cachedSourceFileList) > 0:
            r = random.randrange(0, len(cachedSourceFileList))
            imgName = cachedSourceFileList[r]
            imgPath = os.path.join(self.sourceCache, imgName)
            result = os.path.join(self.sinkCache, imgName)
            Logger.LogInfo(f"Moving image from Source Cache to Sink Cache: {self.driveManager.GetFileNameFromPath(imgName)}")
            f = open(ACTION_LOG, 'a')
            f.write(f"S{imgName}\n")
            f.close()
            os.replace(imgPath, result)
            return result

        return None
