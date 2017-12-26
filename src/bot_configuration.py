import json
import os

_CONSTANT_CONFIG_TOKEN = 'token'
_CONSTANT_CONFIG_GROUP_ID = 'group_id'
_CONSTANT_CONFIG_CHANNEL_NAME = 'channel_name'


class BotConfiguration:
    def __init__(self):
        self._config = None

    def load(self, file):
        file_path = os.path.dirname(__file__) + '/'+ file
        print("[%s] Open file path: %s" %(__name__, file_path))
        with open(file_path) as fd:
            try:
                read_data = fd.read()
                loaded_dict = json.loads(read_data)
                if loaded_dict is not None:
                    self._config = loaded_dict.copy()
            except Exception as e:
                print("[%s] %s" % (__name__, e))

    def get_token(self):
        return self._config[_CONSTANT_CONFIG_TOKEN]

    def get_group_id(self):
        return self._config[_CONSTANT_CONFIG_GROUP_ID]

    def get_channel_name(self):
        return self._config[_CONSTANT_CONFIG_CHANNEL_NAME]

    def info(self):
        print("[%s] Token: %s" %(__name__, self.get_token()))
        print("[%s] Group ID: %s" %(__name__, self.get_group_id()))
        print("[%s] Channel Name: %s" %(__name__, self.get_channel_name()))


