import os
import random

class LocalImageManager:

    def __init__(self, config):
        self.config = config
    
    def GetAllQueuedImages(self):
        return [f for f in os.listdir(self.config["ImgSourceFilePath"]) if any(x in f for x in self.config["SupportedFileTypes"])]
        
    def GetNumberOfQueuedImages(self):
        return len([f for f in os.listdir(self.config["ImgSourceFilePath"]) if any(x in f for x in self.config["SupportedFileTypes"])])

    # This function will first, move the image from the source to the sink
    # Then the path to the image in the sink is returned
    # Will throw a ValueError if no images are in the source
    def PullRandomImageFromSource(self):
        imgs = self.GetAllQueuedImages()
        r = random.randrange(0,len(imgs))
        img = imgs[r]
        imgPath = f"{self.config['ImgSourceFilePath']}\\{img}"
        destinationPath = f"{self.config['ImgSinkFilePath']}\\{img}"
        os.replace(imgPath, destinationPath)

        return destinationPath

    # gets the name of the file
    def GetFileNameFromPath(self, path):
        filename = os.path.basename(path)

        # strip file extention
        for x in self.config["SupportedFileTypes"]: 
            filename = filename.replace(x, "")

        return filename