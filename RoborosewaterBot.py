import json
from Managers.ApiManager import ApiManager
from Managers.DriveImageManager import DriveImageManager

class RoborosewaterBot:

    def __init__(self, api, configPath):
        self.config = json.loads(open(configPath, 'r').read())
        self.api = ApiManager(api)
        self.imageManager = DriveImageManager(self.config)
        
    def Start(self):
        self.SendRandomImageFromSource()

    def SendRandomImageFromSource(self):
        print(self.imageManager.DownloadAndMoveRandomImage())
