import json
from ApiManager import ApiManager

def class RoborosewaterBot:

    def __init__(self, api, configPath):
        self.api = ApiManager(api)
        self.config = json.loads(open(configPath, 'r').read())

    def Start(self):
        while(true):
            # put scheduling logic here
            return