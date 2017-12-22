# Helper to manage forked sub processes
import subprocess

class BotProcess:
    def __init__(self, name, process):
        self._name = name
        self._process = process

    def getName(self):
        return self._name

    def getProcess(self):
        return self._process


class BotPython3ExecutionManager:
    _PYTHON_EXEC_ = 'python3'

    def __init__(self):
        self._runningProcesses = list()

    def getRunningProcessList(self):
        runningProcessNameList = list()

        for process in self._runningProcesses:
            runningProcessNameList.append(process.getName())

        return runningProcessNameList

    def execute(self, pythonFileName, args=None):
        print("[%s] Execute with %s" %(__name__, pythonFileName))
        newProcess = None
        if args != None:
            newProcess = subprocess.Popen([BotPython3ExecutionManager._PYTHON_EXEC_, pythonFileName] + args)
        else:
            newProcess = subprocess.Popen([BotPython3ExecutionManager._PYTHON_EXEC_, pythonFileName])

        if newProcess != None:
            self._runningProcesses.append(BotProcess(pythonFileName, newProcess))
            print("[%s] Forked new process named %s, pid %s" %(__name__, pythonFileName, newProcess.pid))
        else:
            print("[%s] Can't korked new process named %s" %(__name__, pythonFileName))

    def kill(self, processName):
        print("[%s] Kill with %s" %(__name__, processName))
        if len(self._runningProcesses) > 0:
            process = None
            for processIter in self._runningProcesses:
                if processIter.getName() == processName:
                    process = processIter
                    break

            if process != None:
                try:
                    targetProcess = process.getProcess()
                    targetProcess.terminate()
                    targetProcess.wait()
                    self._runningProcesses.remove(process)
                except Exception as e:
                    print("[%s] Exception: %s" %(__name__, e))

    def dispose(self):
        print("[%s] Dispose" %(__name__))
        if len(self._runningProcesses) > 0:
            for process in self._runningProcesses:
                process.terminate()
                process.wait()

            self._runningProcesses.clear()
