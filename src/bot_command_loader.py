# Loader for command json
from bot_command import BotCommand
import json
import os

_CONSTANT_COMMAND_LIST = 'command_list'


class BotCommandLoader:
    def __init__(self):
        self._commands = list()

    def load(self, file):
        file_path = os.path.dirname(__file__) + '/'+ file
        print("[%s] Open file path: %s" %(__name__, file_path))
        with open(file_path) as fd:
            try:
                read_data = fd.read()
                loaded_dict = json.loads(read_data)
                if(_CONSTANT_COMMAND_LIST in loaded_dict):
                    for command in loaded_dict[_CONSTANT_COMMAND_LIST]:
                        self._commands.append(BotCommand(command))
            except Exception as e:
                print("[%s] %s" %(__name__, e))

    def get_list(self):
        return self._commands

    def get_command(self, index=0, name=None):
        if name is not None:
            for command in self._commands:
                if(command.get_name() == name):
                    return command
        else:
            return self._commands[index]

    def get_command_name_list(self):
        name_list = list()
        for command in self._commands:
            name_list.append(command.get_name())

        return name_list

    def size(self):
        return len(self._commands)

    def info(self):
        for command in self._commands:
            command.info()
