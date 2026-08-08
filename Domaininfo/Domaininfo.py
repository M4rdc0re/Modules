from vaelix_host import Agent, RegisterCommand
from struct import pack, calcsize

def dcenum(agentID, *param):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )

    if agent.ProcessArch == "x86":
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "x86 is not supported" )
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to enumerate domain information using Active Directory Domain Services" )
    
    agent.InlineExecute( TaskID, "go", "Domaininfo.o", b'', False )

    return TaskID

RegisterCommand( dcenum, "", "dcenum", "enumerate domain information using Active Directory Domain Services", 0, "", "" )
