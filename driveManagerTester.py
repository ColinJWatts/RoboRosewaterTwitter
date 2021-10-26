from Managers.DriveImageManager import DriveImageManager
import json

config = json.loads(open(".//config.json", 'r').read())
manager = DriveImageManager(config)
print(len(manager.GetListOfAllImageInfo()))
manager.PrintTokenInfo()
manager.RefreshCredentials()
print(len(manager.GetListOfAllImageInfo()))
manager.PrintTokenInfo()