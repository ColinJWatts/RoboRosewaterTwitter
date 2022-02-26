import discord
import threading
import asyncio
from Managers.Logger import Logger
from queue import Queue
from Managers.DiscordClient import DiscordClient

def GetDiscordClientThread(manager,config):
    loop = asyncio.get_event_loop()
    client = DiscordClient(config, manager)
    token = open(config["DiscordTokenFilePath"], 'r').read()
    loop.create_task(client.start(token, bot=config["IsDiscordBotAccount"]))
    return threading.Thread(target=loop.run_forever, daemon=True) #specifying this as a daemon thread makes for smoother shutdown

class DiscordManager:

    def __init__(self, config):
        self.config = config
        Logger.LogInfo("Starting Discord Manager")
        self.messageQueue = Queue()
        self.commandQueue = Queue()
        self.clientThread = GetDiscordClientThread(self, config)
        self.clientThread.start()
        self.client = None

    def SetClient(self, client):
        self.client = client

    # To send a message we simply add it to the message queue
    # this queue will be cleared periodically by the client thread
    def SendMessage(self, text, imageFilePath=None, channel=None):
        message = DiscordMessage(text, imageFilePath, channel)
        self.messageQueue.put(message)

    def GetAllMessagesFromQueue(self):
        result = []
        while not self.messageQueue.empty():
            result.append(self.messageQueue.get())
        return result

    def GetAllCommandsFromQueue(self):
        result = []
        while not self.commandQueue.empty():
            result.append(self.commandQueue.get())
        return result

    def GetTweetChannel(self):
        if self.client is None or self.client.GetTweetChannel() is None: 
            Logger.LogWarning("Could not detect Tweet channel, please reset", self)
            return None
        else: 
            return self.client.tweetChannel      

class DiscordMessage:
    def __init__(self, text, imageFilePath = None, channel = None):
        self.text = text
        self.imageFilePath = imageFilePath
        self.channel = channel

    def HasImage(self):
        if self.imageFilePath is None:
            return False
        return True
    
    def HasChannel(self):
        return not self.channel is None