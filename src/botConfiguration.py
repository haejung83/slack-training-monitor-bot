import json
import os

class BotConfiguration:
    def __init__(self):
        self._config = None

    def load(self, file):
        filePath = os.path.dirname(__file__) + '/'+ file
        print("[%s] Open filepath: %s" %(__name__, filePath))
        with open(filePath) as fd:
            try:
                readData = fd.read()
                loadedDict = json.loads(readData)
                if(loadedDict != None):
                    self._config = loadedDict.copy()
            except:
                print("There is an error with parse the configuration file")

    def getToken(self):
        return self._config['token']

    def getGroupId(self):
        return self._config['group_id']

    def getChannelName(self):
        return self._config['channel_name']

    def info(self):
        print("[%s] Token: %s" %(__name__, self.getToken()))
        print("[%s] Group ID: %s" %(__name__, self.getGroupId()))
        print("[%s] Channel Name: %s" %(__name__, self.getChannelName()))


