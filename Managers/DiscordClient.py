from discord.ext import tasks

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
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        print(message.content)
        # We may be able to pass commands thru here if we want
        if (message.content == self.config["DiscordSetLogChannelCommand"]):
            self.logChannel = message.channel

    @tasks.loop(seconds=5) # Every 5 seconds we try to clear the message queue. can't add this to config with current setup :( 
    async def clear_message_queue(self):
        if (self.logChannel is None):
            print("Log Channel not set, messages not sent")
        else: 
            messages = self.manager.GetAllMessagesFromQueue()
            for m in messages:
                await self.logChannel.send(m)

    @clear_message_queue.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

   

