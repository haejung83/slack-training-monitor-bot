# Containing a command
class BotCommand:
    def __init__(self, command_dict):
        self._command = command_dict

    def getName(self):
        return self._command['name']

    def getCategory(self):
        return self._command['category']

    def getFile(self):
        return self._command['file']

    def getArgs(self):
        return self._command['args']

    def getSplitedArgs(self):
        return self._command['args'].split(' ')

    def info(self):
        print('[%s] Name: %s, Category: %s, File: %s, Args: %s'
              %(__name__, self.getName(), self.getCategory(), self.getFile(), self.getArgs()))