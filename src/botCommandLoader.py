# Loader for command json
from botCommand import BotCommand
import json
import os

class BotCommandLoader:
    def __init__(self):
        self._commands = list()

    def load(self, file):
        filePath = os.path.dirname(__file__) + '/'+ file
        print("[%s] Open filepath: %s" %(__name__, filePath))
        with open(filePath) as fd:
            try:
                readData = fd.read()
                loadedDict = json.loads(readData)
                if(loadedDict != None and 'command_list' in loadedDict):
                    for command in loadedDict['command_list']:
                        self._commands.append(BotCommand(command))
            except:
                print("There is an error with parse the command file")

    def getList(self):
        return self._commands

    def getCommand(self, index=0, name=None):
        if name != None:
            for command in self._commands:
                if(command.getName() == name):
                    return command
        else:
            return self._commands[index]

    def getCommandNameList(self):
        nameList = list()
        for command in self._commands:
            nameList.append(command.getName())

        return nameList

    def size(self):
        return len(self._commands)

    def info(self):
        for command in self._commands:
            command.info()
