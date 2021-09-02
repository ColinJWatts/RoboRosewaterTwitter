import datetime



def AppendToLogFile(logLevel, message, logFile="./logs.txt"):
    f = open(logFile, 'a')
    f.write(f"{logLevel}-{datetime.datetime.now()}: {message}\n")
    f.close()

class Logger():

    @staticmethod
    def LogInfo(message):
        print(message)
        AppendToLogFile("Info", message)

    @staticmethod
    def LogWarning(message, discordManager):
        print(message)
        discordManager.SendMessage(message)
        AppendToLogFile("Warn", message)
    
    @staticmethod
    def LogError(message, discordManager=None):
        print(message)
        AppendToLogFile("Error", message)
        if not discordManager is None:
            discordManager.SendMessage(message)