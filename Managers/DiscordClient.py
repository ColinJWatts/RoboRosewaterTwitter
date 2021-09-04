import os
import discord

from discord.ext import tasks
from Managers.Logger import Logger

class DiscordClient(discord.Client):
    def __init__(self, config, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.manager = manager

        self.logChannel = None

        # start the task to run in the background
        self.clear_message_queue.start()

    async def on_ready(self):
        Logger.LogInfo(f'Logged in as {self.user} (ID: {self.user.id})')
        # try to load log channel from cache (if it exists)
        # note, this will try to cache PM channels and then fail to load them (only works for guild channels)
        if os.path.isfile(self.config["LogChannelCachePath"]):
            logChannelId = open(self.config["LogChannelCachePath"]).read()
            self.logChannel = self.get_channel(int(logChannelId))
            if not self.logChannel is None:
                Logger.LogInfo(f'Log Channel ({self.logChannel.name}) loaded frocm cache')
            else: 
                Logger.LogInfo("Failed to load Log Channel from Cache, please reset")


    async def on_message(self, message):
        # We may be able to pass commands thru here if we want
        if (message.content == self.config["DiscordSetLogChannelCommand"]):
            Logger.LogInfo("Log Channel Set")
            self.logChannel = message.channel
            # cache log channel
            f = open(self.config["LogChannelCachePath"], 'w')
            f.write(f"{self.logChannel.id}")
            f.close()

    @tasks.loop(seconds=5) # Every 5 seconds we try to clear the message queue. can't add this to config with current setup :( 
    async def clear_message_queue(self):
        if (self.logChannel is None):
            if self.manager.messageQueue.qsize() > 0:
                Logger.LogInfo("Log Channel not set, messages not sent")
        else: 
            messages = self.manager.GetAllMessagesFromQueue()
            for m in messages:
                if m.HasImage():
                    await self.logChannel.send(m.text, file=discord.File(m.imageFilePath))
                else:
                    await self.logChannel.send(m.text)

    @clear_message_queue.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

   

