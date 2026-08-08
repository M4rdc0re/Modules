"""Reference stubs for module registration scripts.

Vaelix does not load these Python files — the teamserver registers BOF/DLL
commands natively in Go. This module exists so the .py stubs no longer depend
on an external host API named after another framework.
"""


class Agent:
    CONSOLE_TASK = 0
    CONSOLE_ERROR = 1
    CONSOLE_INFO = 2
    CONSOLE_GOOD = 3

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.ProcessArch = "x64"
        self.OSArch = "x64"

    def ConsoleWrite(self, _kind, message):
        return message

    def InlineExecute(self, *_args, **_kwargs):
        return None

    def DllSpawn(self, *_args, **_kwargs):
        return None

    def Command(self, *_args, **_kwargs):
        return None


def RegisterCommand(*_args, **_kwargs):
    return None


def RegisterModule(*_args, **_kwargs):
    return None


def RegisterCallback(*_args, **_kwargs):
    return None
