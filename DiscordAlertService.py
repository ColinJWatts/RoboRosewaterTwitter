import discord
import queue

client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        data = message.content[1:len(message.content)].split()
        print(data)

class DiscordClientThread (threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.token = token

    def run(self):
        print(f"Starting DiscordClientThread")
        client.run(self.token)

class DiscordAlertService: 
    def __init__(self, config):
        self.config = config
        self.messageQueue = Queue()

        discordToken = open(self.config["DiscordTokenPath"], 'r').read()
        self.clientThread = DiscordClientThread(discordToken)
        self.clientThread.start()

    def SendMessage(self, message):
        self.messageQueue.put(message)