import discord
import threading
import asyncio
from Managers.Logger import Logger
from queue import Queue
from Managers.DiscordClient import DiscordClient

def run_discord_client_thread(manager,config):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = DiscordClient(config, manager)
    client.run(open(config["DiscordTokenFilePath"], 'r').read())

class DiscordManager:

    def __init__(self, config):
        self.config = config
        Logger.LogInfo("Starting Discord Manager")
        self.messageQueue = Queue()
        self.clientThread = threading.Thread(target=run_discord_client_thread, args=(self,config,))
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