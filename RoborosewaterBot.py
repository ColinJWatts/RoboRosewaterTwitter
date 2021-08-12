import json
from Managers.ApiManager import ApiManager
from Managers.ImageManager import ImageManager

class RoborosewaterBot:

    def __init__(self, api, configPath):
        self.config = json.loads(open(configPath, 'r').read())
        self.api = ApiManager(api)
        self.imageManager = ImageManager(self.config)
        
    def Start(self):
        self.SendRandomImageFromSource()

    # NOTE: this isn't intended to be a final solution, just an example of how to use the managers
    def SendRandomImageFromSource(self):
        imgPath = self.imageManager.PullRandomImageFromSource()
        filename = self.imageManager.GetFileNameFromPath(imgPath)
        self.api.SendImageAsTweet(imgPath, filename)