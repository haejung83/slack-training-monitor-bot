# Helper to manage forked sub processes
import subprocess


class BotProcess:
    def __init__(self, name, process):
        self._name = name
        self._process = process

    def get_name(self):
        return self._name

    def get_process(self):
        return self._process


class BotExecutionManager:
    _PYTHON_EXEC_ = 'python3'

    def __init__(self):
        self._runningProcesses = list()

    def get_running_processes(self):
        process_list = list()

        for process in self._runningProcesses:
            process_list.append(process.get_name())

        return process_list

    def execute(self, exec_file_name, args=None):
        print("[%s] Execute %s" %(__name__, exec_file_name))
        if args is not None:
            new_process = subprocess.Popen([BotExecutionManager._PYTHON_EXEC_, exec_file_name] + args)
        else:
            new_process = subprocess.Popen([BotExecutionManager._PYTHON_EXEC_, exec_file_name])

        if new_process is not None:
            self._runningProcesses.append(BotProcess(exec_file_name, new_process))
            print("[%s] Forked new process named %s, pid %s" %(__name__, exec_file_name, new_process.pid))
        else:
            print("[%s] Can't korked new process named %s" %(__name__, exec_file_name))

    def kill(self, process_name):
        print("[%s] Kill with %s" %(__name__, process_name))
        if len(self._runningProcesses) > 0:
            process = None
            for processIter in self._runningProcesses:
                if processIter.get_name() == process_name:
                    process = processIter
                    break

            if process is not None:
                print("[%s] Found out alive process %s" %(__name__, process_name))
                try:
                    target_process = process.get_process()
                    target_process.terminate()
                    target_process.wait()
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
