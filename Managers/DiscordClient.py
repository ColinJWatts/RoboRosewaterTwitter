from discord.ext import tasks
from Managers.Logger import Logger

import discord

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

    async def on_message(self, message):
        # We may be able to pass commands thru here if we want
        if (message.content == self.config["DiscordSetLogChannelCommand"]):
            Logger.LogInfo("Log Channel Set")
            self.logChannel = message.channel

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

   

