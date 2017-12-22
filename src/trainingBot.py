import json
import websockets
import asyncio
from slacker import Slacker
from botPython3ExecutionManager import BotPython3ExecutionManager

_CONSTANT_USAGE_PREFIX = 'Commands :\n\tlist\n\tstatus\n\trun <commands>\n\tstop <command>'
_CONSTANT_ENABLE_LOG = 'enable_log'

class RequestCommand:
    def __init__(self, type, param):
        self._type = type
        self._param = param

    def getType(self):
        return self._type

    def getParam(self):
        return self._param

class RequestCommandParser:
    def __init__(self):
        pass

    def parse(self, rawCommand):
        slicedRequestCommand = rawCommand.split(' ')
        if len(slicedRequestCommand) > 0:
            type = slicedRequestCommand[0]
            param = slicedRequestCommand[1:]
            return RequestCommand(type, param)
        else:
            return None

class TrainingBot:
    def __init__(self, config, cmdLoader):
        self._config = config
        self._cmdLoader = cmdLoader
        self._isRunningLoop = False
        self._executionManager = BotPython3ExecutionManager()
        self._requestCommandParser = RequestCommandParser()
        self._flag = dict()
        self._setupFlag()

    def _setupFlag(self):
        self._flag[_CONSTANT_ENABLE_LOG] = True

    def _buildSlacker(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Build Slacker" %(__name__))

        if not hasattr(self, '_config'):
            raise Exception("Not available configuration")

        return Slacker(self._config.getToken())

    def _buildDefaultMessageDict(self):
        self._defaultMessageDict = {
            'id': '1',
            'type': 'message',
            'channel': self._config.getGroupId(),
            'text': _CONSTANT_USAGE_PREFIX,
        }

    def _connect(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Connect" %(__name__))

        if not hasattr(self, '_slacker'):
            self._slacker = self._buildSlacker()

        response = self._slacker.rtm.start()
        return response

    def _disconnect(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Disconnect" %(__name__))

    def _setResult(self, result):
        self._defaultMessageDict['text'] = result

    def _dispatchCommand(self, command):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Dispatch Command: %s" %(__name__, command))

        reqCommand = self._requestCommandParser.parse(command)
        reqType = reqCommand.getType()
        reqParam = reqCommand.getParam()

        if reqType == 'list':
            cmdListString = str()
            for cmd in self._cmdLoader.getCommandNameList():
                cmdListString += cmd + '\n'

            self._setResult(cmdListString)
        elif reqType == 'run':
            if len(reqParam) > 0:
                self._setResult("Run with " + reqParam[0])
                executionCommand = self._cmdLoader.getCommand(name=reqParam[0])
                self._executionManager.execute(executionCommand.getFile(), args=executionCommand.getSplitedArgs())
            else:
                self._setResult("Can't run with given command!")

        elif reqType == 'stop':
            if len(reqParam) > 0:
                self._setResult("Stopped " + reqParam[0])
                executionCommand = self._cmdLoader.getCommand(name=reqParam[0])
                self._executionManager.kill(executionCommand.getFile())
            else:
                self._setResult("Can't run with given command!")

        else:
            return False

        return True

    # Async loop
    async def _loop(self):
        if self._flag[_CONSTANT_ENABLE_LOG]:
            print("[%s] Start loop" %(__name__))

        if not hasattr(self, '_defaultMessageDict'):
            self._buildDefaultMessageDict()

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
                parsedMessage = json.loads(message_json)
                if 'type' in parsedMessage:
                    if parsedMessage['type'] == 'message':
                        if self._dispatchCommand(parsedMessage['text']):
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

