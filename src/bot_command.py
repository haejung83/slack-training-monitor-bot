# Containing a command
_CONSTANT_COMMAND_NAME = 'name'
_CONSTANT_COMMAND_CATEGORY = 'category'
_CONSTANT_COMMAND_FILE = 'file'
_CONSTANT_COMMAND_ARGS = 'args'


class BotCommand:
    def __init__(self, command_dict):
        self._command = command_dict

    def get_name(self):
        return self._command[_CONSTANT_COMMAND_NAME]

    def get_category(self):
        return self._command[_CONSTANT_COMMAND_CATEGORY]

    def get_file(self):
        return self._command[_CONSTANT_COMMAND_FILE]

    def get_args(self):
        return self._command[_CONSTANT_COMMAND_ARGS]

    def get_split_args(self):
        return self._command[_CONSTANT_COMMAND_ARGS].split(' ')

    def info(self):
        print('[%s] Name: %s, Category: %s, File: %s, Args: %s'
              %(__name__, self.get_name(), self.get_category(), self.get_file(), self.get_args()))