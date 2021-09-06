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
        self.clientThread = GetDiscordClientThread(self, config)
        self.clientThread.start()

    # To send a message we simply add it to the message queue
    # this queue will be cleared periodically by the client thread
    def SendMessage(self, text, imageFilePath=None):
        message = DiscordMessage(text, imageFilePath)
        self.messageQueue.put(message)

    def GetAllMessagesFromQueue(self):
        result = []
        while not self.messageQueue.empty():
            result.append(self.messageQueue.get())
        return result

class DiscordMessage:
    def __init__(self, text, imageFilePath = None):
        self.text = text
        self.imageFilePath = imageFilePath

    def HasImage(self):
        if self.imageFilePath is None:
            return False
        return True