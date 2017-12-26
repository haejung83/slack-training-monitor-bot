import json
import websockets
import asyncio
from slacker import Slacker
from bot_execution_manager import BotExecutionManager

_CONSTANT_USAGE_PREFIX = 'Commands :\n\tlist\n\tstatus\n\trun <commands>\n\tstop <command>'
_CONSTANT_ENABLE_LOG = 'enable_log'


class RequestCommand:
    def __init__(self, type, param):
        self._type = type
        self._param = param

    def get_type(self):
        return self._type

    def get_param(self):
        return self._param


class RequestCommandParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(raw_command):
        partial_request_command = raw_command.split(' ')
        if len(partial_request_command) > 0:
            req_type = partial_request_command[0]
            req_param = partial_request_command[1:]
            return RequestCommand(req_type, req_param)
        else:
            return None


class TrainingBot:
    def __init__(self, config, cmdLoader):
        self._config = config
        self._cmdLoader = cmdLoader
        self._isRunningLoop = False
        self._executionManager = BotExecutionManager()
        self._flag = dict()
        self._sock_endpoint = None
        self._setup_flag()

    def _setup_flag(self):
        self._flag[_CONSTANT_ENABLE_LOG] = True

    def _build_slacker(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Build Slacker" %(__name__))

        if not hasattr(self, '_config'):
            raise Exception("Not available configuration")

        return Slacker(self._config.get_token())

    def _build_default_message_dict(self):
        self._defaultMessageDict = {
            'id': '1',
            'type': 'message',
            'channel': self._config.get_group_id(),
            'text': _CONSTANT_USAGE_PREFIX,
        }

    def _connect(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Connect" %(__name__))

        if not hasattr(self, '_slacker'):
            self._slacker = self._build_slacker()

        response = self._slacker.rtm.start()
        return response

    def _disconnect(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Disconnect" %(__name__))

    def _set_result(self, result):
        self._defaultMessageDict['text'] = result

    def _dispatch_command(self, command):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Dispatch Command: %s" %(__name__, command))

        req_command = RequestCommandParser.parse(command)
        req_type = req_command.get_type()
        req_param = req_command.get_param()

        if req_type == 'list':
            cmd_list_str = str()
            for cmd in self._cmdLoader.get_command_name_list():
                cmd_list_str += cmd + '\n'

            self._set_result(cmd_list_str)
        elif req_type == 'run':
            if len(req_param) > 0:
                self._set_result("Run with " + req_param[0])
                exec_command = self._cmdLoader.get_command(name=req_param[0])
                self._executionManager.execute(exec_command.get_file(), args=exec_command.get_split_args())
            else:
                self._set_result("Can't run with given command!")
        elif req_type == 'stop':
            if len(req_param) > 0:
                self._set_result("Stopped " + req_param[0])
                exec_command = self._cmdLoader.get_command(name=req_param[0])
                self._executionManager.kill(exec_command.get_file())
            else:
                self._set_result("Can't run with given command!")
        elif req_type == 'status':
            # TODO : Not implemented yet
            self._set_result('Check a status')
        else:
            self._build_default_message_dict()

        return True

    # Async loop
    async def _loop(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Start loop" %(__name__))

        if not hasattr(self, '_defaultMessageDict'):
            self._build_default_message_dict()

        ws = await websockets.connect(self._sock_endpoint)

        # Wait an ack
        await ws.recv()
        # Send a command list
        await ws.send(json.dumps(self._defaultMessageDict))

        while self._isRunningLoop:
            message_json = await ws.recv()

            #if self._flag[_CONSTANT_ENABLE_LOG]:
            #    print('[%s] Received: %s' %(__name__, message_json))

            try:
                parsed_msg = json.loads(message_json)
                if 'type' in parsed_msg:
                    if parsed_msg['type'] == 'message':
                        if self._dispatch_command(parsed_msg['text']):
                            await ws.send(json.dumps(self._defaultMessageDict))
            except Exception as e:
                print("[%s] Exception: %s" %(__name__, e))

    def start(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Start" %(__name__))

        self._isRunningLoop = True

        response = self._connect()
        self._sock_endpoint = response.body['url']

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self._loop())

    def stop(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Stop" %(__name__))

        self._isRunningLoop = False
        self._executionManager.dispose()
        self._disconnect()

