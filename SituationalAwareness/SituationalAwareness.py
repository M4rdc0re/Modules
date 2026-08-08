from vaelix_host import Agent, RegisterCommand

def arp( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite(agent.CONSOLE_TASK, "Tasked agent to lists out ARP table")

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/arp.{agent.ProcessArch}.o", b'', False )

    return TaskID

def driversigs( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite(agent.CONSOLE_TASK, "Tasked agent to check drivers for known edr vendor names")

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/driversigs.{agent.ProcessArch}.o", b'', False )

    return TaskID

def ipconfig( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite(agent.CONSOLE_TASK, "Tasked agent to lists out adapters, system hostname and configured dns serve")

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/ipconfig.{agent.ProcessArch}.o", b'', False )

    return TaskID

def listdns( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to lists dns cache entries" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/listdns.{agent.ProcessArch}.o", b'', False )

    return TaskID

def locale( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite(agent.CONSOLE_TASK, "Tasked agent to retrieve system locale information, date format, and country")

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/locale.{agent.ProcessArch}.o", b'', False )

    return TaskID

def netstat( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to get local ipv4 udp/tcp listening and connected ports" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netstat.{agent.ProcessArch}.o", b'', False )

    return TaskID

def resources( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list available memory and space on the primary disk drive" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/resources.{agent.ProcessArch}.o", b'', False )

    return TaskID

def routeprint( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to prints ipv4 routes on the machine" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/routeprint.{agent.ProcessArch}.o", b'', False )

    return TaskID

def uptime( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to lists system boot time" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/uptime.{agent.ProcessArch}.o", b'', False )

    return TaskID

def whoami( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to get the info from whoami /all without starting cmd.exe" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/whoami.{agent.ProcessArch}.o", b'', False )

    return TaskID

def windowlist( agentID, *param ):
    TaskID : str    = None
    agent  : Agent  = None

    agent  = Agent( agentID )
    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list windows visible on the users desktop" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/windowlist.{agent.ProcessArch}.o", b'', False )

    return TaskID

def reg_query_parse_params( agent, params ):
    packer = Packer()

    reghives = {
        'HKCR': 0,
        'HKCU': 1,
        'HKLM': 2,
        'HKU': 3
    }

    num_params = len(params)
    params_parsed = 0

    if num_params < 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Missing parameters" )
        return None

    if num_params > 4:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    if params[ params_parsed ].upper() not in reghives:
        hostname = params[ params_parsed ]
        params_parsed += 1
    else:
        hostname = None

    if params[ params_parsed ].upper() not in reghives:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Provided registry hive value is invalid" )
        return None

    hive = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    if num_params < params_parsed + 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Missing parameters" )
        return None

    path = params[ params_parsed ]
    params_parsed += 1

    if num_params > params_parsed:
        key = params[ params_parsed ]
    else:
        key = None

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.addbool(False) # recursive

    return packer.getbuffer()

def reg_query( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = reg_query_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to query the windows registry" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/reg_query.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def reg_query_recursive_parse_params( agent, params ):
    packer = Packer()

    reghives = {
        'HKCR': 0,
        'HKCU': 1,
        'HKLM': 2,
        'HKU': 3
    }

    num_params = len(params)
    params_parsed = 0

    if num_params < 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Missing parameters" )
        return None

    if num_params > 3:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    if params[ params_parsed ].upper() not in reghives:
        hostname = params[ params_parsed ]
        params_parsed += 1
    else:
        hostname = None

    if params[ params_parsed ].upper() not in reghives:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Provided registry hive value is invalid" )
        return None

    hive = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    if num_params < params_parsed + 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Missing parameters" )
        return None

    path = params[ params_parsed ]

    key = None

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.addbool(True) # recursive

    return packer.getbuffer()

def reg_query_recursive( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    packer = Packer()
    agent  = Agent( agentID )

    packed_params = reg_query_recursive_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to query the windows registry recursively" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/reg_query.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def wmi_query_parse_params( agent, params ):
    packer = Packer()

    query     = ''
    server    = '.'
    namespace = 'root\\cimv2'

    num_params = len(params)

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Missing parameters" )
        return None

    if num_params > 3:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    query = params[ 0 ]

    if num_params > 1:
        server = params[ 1 ]

    if num_params > 2:
        namespace = params[ 2 ]

    resource = f"\\\\{server}\\{namespace}"

    packer.addWstr(server)
    packer.addWstr(namespace)
    packer.addWstr(query)
    packer.addWstr(resource)

    return packer.getbuffer()

def wmi_query( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = wmi_query_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to query the Windows Management Toolkit" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/wmi_query.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def nslookup_parse_params( agent, params ):
    packer = Packer()

    recordmapping = {
        'A': 1,
        'NS': 2,
        'MD': 3,
        'MF': 4,
        'CNAME': 5,
        'SOA': 6,
        'MB': 7,
        'MG': 8,
        'MR': 9,
        'WKS': 0xb,
        'PTR': 0xc,
        'HINFO': 0xd,
        'MINFO': 0xe,
        'MX': 0xf,
        'TEXT': 0x10,
        'RP': 0x11,
        'AFSDB': 0x12,
        'X25': 0x13,
        'ISDN': 0x14,
        'RT': 0x15,
        'AAAA': 0x1c,
        'SRV': 0x21,
        'WINSR': 0xff02,
        'KEY': 0x0019,
        'ANY': 0xff
    }

    num_params = len(params)
    lookup = ''
    server = ''
    _type   = recordmapping[ 'A' ]

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Missing parameters" )
        return None

    lookup = params[ 0 ]

    if num_params > 1:
        server = params[ 1 ]
        if server == '127.0.0.1':
            agent.ConsoleWrite( agent.CONSOLE_ERROR, "Localhost dns query's have a potential to crash, refusing" )
            return None

    if num_params > 2 and params[ 2 ].upper() in recordmapping:
        _type = recordmapping[ params[ 2 ].upper() ]

    if num_params > 3:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(lookup)
    packer.addstr(server)
    packer.addshort(_type)

    return packer.getbuffer()

def nslookup( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = nslookup_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to run DNS query" )

    # nslookup can hang, so let's run it in threaded mode
    agent.InlineExecute( TaskID, "go", f"ObjectFiles/nslookup.{agent.ProcessArch}.o", packed_params, True )

    return TaskID

def env( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to obtain the environment variables for the current process" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/env.{agent.ProcessArch}.o", b'', False )

    return TaskID

def get_password_policy_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    hostname = '.'

    if num_params == 1:
        hostname = params[ 0 ]

    if num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(hostname)

    return packer.getbuffer()

def get_password_policy( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = get_password_policy_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to obtain the password policy" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/get_password_policy.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def list_firewall_rules( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    packer = Packer()
    agent  = Agent( agentID )

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list all firewall rules" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/get_password_policy.{agent.ProcessArch}.o", b'', False )

    return TaskID

def cacls_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None

    filepath = params[ 0 ]

    if num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(filepath)

    return packer.getbuffer()

def cacls( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = cacls_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to obtain file permissions" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/cacls.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def schtasksenum_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    server = ''

    if num_params == 1:
        server = params[ 0 ]

    if num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(server)

    return packer.getbuffer()

def schtasksenum( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = schtasksenum_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list all scheduled tasks" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/schtasksenum.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def schtasksquery_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        server = params[ 0 ]
        service = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(server)
    packer.addWstr(service)

    return packer.getbuffer()

def schtasksquery( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = schtasksquery_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to query a given scheduled task" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/schtasksquery.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_enum_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    server = ''

    if num_params == 1:
        server = params[ 0 ]

    if num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)

    return packer.getbuffer()

def sc_enum( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = sc_enum_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to enumerate all service configs" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/sc_enum.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qc_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qc( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = sc_qc_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to run sc qc" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qc.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_query_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        pass
    elif num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_query( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = sc_query_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to run sc query" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/sc_query.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qdescription_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qdescription( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = sc_qdescription_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to get the description of a service" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qdescription.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qfailure_get_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qfailure( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = sc_qfailure_get_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to get the failure reason for a service" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qfailure.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qtriggerinfo_get_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qtriggerinfo( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = sc_qtriggerinfo_get_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to get the failure reason for a service" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qtriggerinfo.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def adcs_enum_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    domain = ''

    if num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params == 1:
        domain = params[ 0 ]

    packer.addWstr(domain)

    return packer.getbuffer()

def adcs_enum( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = adcs_enum_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to enumerate CAs and templates in the AD" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/adcs_enum.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def enumlocalsessions( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    num_params = len(params)

    if num_params > 0:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to enumerate currently attached user sessions both local and over RDP" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/enumlocalsessions.{agent.ProcessArch}.o", b'', False )

    return TaskID

def enum_filter_driver_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    system = ''

    if num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params == 1:
        system = params[ 0 ]

    packer.addstr(system)

    return packer.getbuffer()

def enum_filter_driver( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = enum_filter_driver_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to enumerate filter drivers" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/enum_filter_driver.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def ldapsearch_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)

    query = ''
    attributes = ''
    result_limit = 0
    hostname = ''
    domain = ''

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params > 5:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    query = params[ 0 ]

    if num_params >= 2:
        attributes = params[ 1 ]

    if num_params >= 3:
        result_limit = int( params[ 2 ] )

    if num_params >= 4:
        hostname = params[ 3 ]

    if num_params >= 5:
        domain = params[ 4 ]

    packer.addstr(query)
    packer.addstr(attributes)
    packer.adduint32(result_limit)
    packer.addstr(hostname)
    packer.addstr(domain)

    return packer.getbuffer()

def ldapsearch( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = ldapsearch_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to run ldap query" )

    # ldapsearch can hang, so let's run it in threaded mode
    agent.InlineExecute( TaskID, "go", f"ObjectFiles/ldapsearch.{agent.ProcessArch}.o", packed_params, True )

    return TaskID

def netsession_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(computer)

    return packer.getbuffer()

def netsession( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netsession_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to enumerate sessions on the local or specified computer" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/get-netsession.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netGroupList_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    domain = ''
    group = ''

    if num_params == 1:
        domain = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(0)
    packer.addWstr(domain)
    packer.addWstr(group)

    return packer.getbuffer()

def netGroupList( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netGroupList_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list groups from the default or specified domain" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netgroup.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netGroupListMembers_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    domain = ''
    group = ''

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None
    elif num_params == 1:
        group = params[ 0 ]
    elif num_params == 2:
        domain = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(1)
    packer.addWstr(domain)
    packer.addWstr(group)

    return packer.getbuffer()

def netGroupListMembers( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netGroupListMembers_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list group members from the default or specified domain" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netgroup.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netLocalGroupList_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    server = ''
    group = ''

    if num_params == 1:
        server = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(0)
    packer.addWstr(server)
    packer.addWstr(group)

    return packer.getbuffer()

def netLocalGroupList( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netLocalGroupList_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list local groups from the local or specified computer" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netlocalgroup.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netLclGrpLstMmbrs_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    domain = ''
    group = ''

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None
    elif num_params == 1:
        group = params[ 0 ]
    elif num_params == 2:
        group = params[ 0 ]
        domain = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(1)
    packer.addWstr(domain)
    packer.addWstr(group)

    return packer.getbuffer()

def netLclGrpLstMmbrs( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netLclGrpLstMmbrs_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list local group members" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netlocalgroup.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netuser_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    username = ''
    domain = ''

    if num_params < 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Not enough parameters" )
        return None
    elif num_params == 1:
        username = params[ 0 ]
    elif num_params == 2:
        username = params[ 0 ]
        domain = params[ 1 ]
    else:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(username)
    packer.addWstr(domain)

    return packer.getbuffer()

def netuser( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netuser_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to get info about specific user" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netuser.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def userenum_parse_parans( agent, params ):
    packer = Packer()

    num_params = len(params)

    enumtype = {
        'all': 1,
        'locked': 2,
        'disabled': 3,
        'active': 4
    }

    _type = enumtype[ 'all' ]

    if num_params == 1:
        if params[ 0 ].lower() not in enumtype:
            agent.ConsoleWrite( agent.CONSOLE_ERROR, "Parameter not in: [all, locked, disabled, active]" )
            return None
        _type = enumtype[ params[ 0 ].lower() ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.adduint32(0)
    packer.adduint32(_type)

    return packer.getbuffer()

def userenum( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = userenum_parse_parans( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list user accounts on the current computer" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netuserenum.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def domainenum_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)

    enumtype = {
        'all': 1,
        'locked': 2,
        'disabled': 3,
        'active': 4
    }

    _type = enumtype[ 'all' ]

    if num_params == 1:
        if params[ 0 ].lower() not in enumtype:
            agent.ConsoleWrite( agent.CONSOLE_ERROR, "Parameter not in: [all, locked, disabled, active]" )
            return None
        _type = enumtype[ params[ 0 ].lower() ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.adduint32(1)
    packer.adduint32(_type)

    return packer.getbuffer()

def domainenum( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = domainenum_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list user accounts in the current domain" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netuserenum.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netshares_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return False

    packer.addWstr(computer)
    packer.adduint32(0)

    return packer.getbuffer()

def netshares( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netshares_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list shares on local or remote computer" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netshares.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netsharesAdmin_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(computer)
    packer.adduint32(1)

    return packer.getbuffer()

def netsharesAdmin( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netsharesAdmin_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list shares on local or remote computer" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netshares.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netuptime_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    hostname = ''

    if num_params == 1:
        hostname = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(hostname)

    return packer.getbuffer()

def netuptime( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netuptime_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list local workstations and servers" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netuptime.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def netview_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(computer)

    return packer.getbuffer()

def netview( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = netview_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, "Tasked agent to list local workstations and servers" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/netview.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def quser_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    hostname   = ''

    if num_params < 1:
        hostname = '127.0.0.1'
    elif num_params == 1:
        hostname = params[ 0 ]
    elif num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(hostname)

    return packer.getbuffer(), hostname

def quser( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params, hostname = quser_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to obtain the list RDP connections on {hostname}" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/quser.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def bofdir_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    targetdir  = '.\\'
    subdirs    = 0

    if num_params > 2:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params > 0:
        targetdir = params[0]

    if num_params == 2 and params[1] != '/s':
        agent.ConsoleWrite( agent.CONSOLE_ERROR, f"Invalid parameter: {params[1]}" )
        return None

    if num_params == 2 and params[1] == '/s':
        subdirs = 1

    packer.addWstr(targetdir)
    packer.addshort(subdirs)

    return packer.getbuffer()

def bofdir( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = bofdir_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent to list a directory" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/dir.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

def tasklist_parse_params( agent, params ):
    packer = Packer()

    num_params = len(params)
    hostname   = ''

    if num_params > 1:
        agent.ConsoleWrite( agent.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params > 0:
        hostname = params[0]

    packer.addWstr(hostname)

    return packer.getbuffer()

def sa_tasklist( agentID, *params ):
    TaskID : str    = None
    agent  : Agent  = None
    agent  = Agent( agentID )

    packed_params = tasklist_parse_params( agent, params )
    if packed_params is None:
        return False

    TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"Tasked agent list running processes" )

    agent.InlineExecute( TaskID, "go", f"ObjectFiles/tasklist.{agent.ProcessArch}.o", packed_params, False )

    return TaskID

RegisterCommand( arp, "", "arp", "Lists out ARP table", 0, "", "" )
RegisterCommand( driversigs, "", "driversigs", "checks drivers for known edr vendor names", 0, "", "" )
RegisterCommand( ipconfig, "", "ipconfig", "Lists out adapters, system hostname and configured dns serve", 0, "", "" )
RegisterCommand( listdns, "", "listdns", "lists dns cache entries", 0, "", "" )
RegisterCommand( locale, "", "locale", "Prints locale information", 0, "", "" )
RegisterCommand( netstat, "", "netstat", "List listening and connected ipv4 udp and tcp connections", 0, "", "" )
RegisterCommand( resources, "", "resources", "list available memory and space on the primary disk drive", 0, "", "" )
RegisterCommand( routeprint, "", "routeprint", "prints ipv4 routes on the machine", 0, "", "" )
RegisterCommand( uptime, "", "uptime", "lists system boot time", 0, "", "" )
RegisterCommand( whoami, "", "whoami", "get the info from whoami /all without starting cmd.exe", 0, "", "" )
RegisterCommand( windowlist, "", "windowlist", "list windows visible on the users desktop", 0, "[opt:all]", "" )
RegisterCommand( reg_query, "", "reg_query", "Query a registry value or enumerate a single key", 0, "[opt:hostname] [hive] [path] [opt: value to query]", "HKLM SYSTEM\\CurrentControlSet\\Control\\Lsa RunAsPPL" )
RegisterCommand( reg_query_recursive, "", "reg_query_recursive", "Recursively enumerate a key starting at path", 0, "[opt:hostname] [hive] [path]", "HKLM SYSTEM\\CurrentControlSet\\Control\\Lsa" )
RegisterCommand( wmi_query, "", "wmi_query", "Run a wmi query and display results in CSV format", 0, "query [opt: server] [opt: namespace]", "\"Select name from Win32_ComputerSystem\"" )
RegisterCommand( nslookup, "", "nslookup", "Make a DNS query. DNS server is the server you want to query (do not specify or 0 for default). Record type is something like A, AAAA, or ANY", 0, "hostname [opt:dns server] [opt: record type]", "dc01" )
RegisterCommand( env, "", "env", "Print environment variables.", 0, "", "" )
RegisterCommand( get_password_policy, "", "get_password_policy", "Gets a server or DC's configured password policy", 0, "[hostname]", "" )
#RegisterCommand( list_firewall_rules, "", "list_firewall_rules", "List Windows firewall rules", 0, "", "" )
RegisterCommand( cacls, "", "cacls", "List user permissions for the specified file, wildcards supported", 0, "[filepath]", "C:\\Windows\\Temp\\test.txt" )
RegisterCommand( schtasksenum, "", "schtasksenum", "Enumerate scheduled tasks on the local or remote computer", 0, "[opt: server]", "" )
RegisterCommand( schtasksquery, "", "schtasksquery", "Query the given task on the local or remote computer", 0, "[opt: server] [taskpath]", "" )
RegisterCommand( sc_enum, "", "sc_enum", "Enumerate services for qc, query, qfailure, and qtriggers info", 0, "[opt: server]", "" )
RegisterCommand( sc_qc, "", "sc_qc", "sc qc impelmentation in BOF", 0, "service_name [opt:server]", "SensorService" )
RegisterCommand( sc_query, "", "sc_query", "sc query implementation in BOF", 0, "[opt: service name] [opt: server]", "" )
RegisterCommand( sc_qdescription, "", "sc_qdescription", "Queries a services description", 0, "service_name [opt: server]", "SensorService" )
RegisterCommand( sc_qfailure, "", "sc_qfailure", "Query a service for failure conditions", 0, "service_name [opt: server]", "SensorService" )
RegisterCommand( sc_qtriggerinfo, "", "sc_qtriggerinfo", "Query a service for trigger conditions", 0, "service_name [opt: server]", "SensorService" )
RegisterCommand( adcs_enum, "", "adcs_enum", "Enumerate CAs and templates in the AD using Win32 functions", 0, "[opt: domain]", "" )
RegisterCommand( enumlocalsessions, "", "enumlocalsessions", "Enumerate currently attached user sessions both local and over RDP", 0, "", "" )
RegisterCommand( enum_filter_driver, "", "enum_filter_driver", "Enumerate filter drivers", 0, "[opt: system]", "" )
RegisterCommand( ldapsearch, "", "ldapsearch", "Execute LDAP searches (NOTE: specify *,ntsecuritydescriptor as attribute parameter if you want all attributes + base64 encoded ACL of the objects, this can then be resolved using BOFHound. Could possibly break pagination, although everything seemed fine during testing.)", 0, "query [opt: attribute] [opt: results_limit] [opt: DC hostname or IP] [opt: Distingished Name]", "\"(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304))\"" )
RegisterCommand( netsession, "", "get-netsession", "Enumerate sessions on the local or specified computer", 0, "[opt:computer]", "" )
RegisterCommand( netGroupList, "", "netGroupList", "List groups from the default or specified domain", 0, "[opt: domain]", "" )
RegisterCommand( netGroupListMembers, "", "netGroupListMembers", "List group members from the default or specified domain", 0, "groupname [opt: domain]", "" )
RegisterCommand( netLocalGroupList, "", "netLocalGroupList", "List local groups from the local or specified computer", 0, "[opt: server]", "" )
RegisterCommand( netLclGrpLstMmbrs, "", "netLclGrpLstMmbrs", "List local group members from the local or specified group", 0, "groupname [opt: server]", "Administrators" )
RegisterCommand( netuser, "", "netuser", "Get info about specific user. Pull from domain if a domainname is specified", 0, "username [opt: domain]", "Administrator" )
RegisterCommand( userenum, "", "userenum", "Lists user accounts on the current computer", 0, "[opt: <all,locked,disabled,active>]", "" )
RegisterCommand( domainenum, "", "domainenum", "Lists users accounts in the current domain", 0, "[opt: <all,locked,disabled,active>]", "" )
RegisterCommand( netshares, "", "netshares", "List shares on local or remote computer", 0, "<\\\\computername>", "" )
RegisterCommand( netshares, "", "netshares", "List shares on local or remote computer", 0, "[opt: \\\\computername]", "" )
RegisterCommand( netsharesAdmin, "", "netsharesAdmin", "List shares on local or remote computer and gets more info then standard netshares (requires admin)", 0, "[opt: \\\\computername]", "" )
RegisterCommand( netuptime, "", "netuptime", "Returns information about the boot time on the local (or a remote) machine", 0, "[opt: hostname]", "" )
RegisterCommand( netview, "", "netview", "lists local workstations and servers", 0, "[opt: netbios_domain_name]", "" )
RegisterCommand( quser, "", "quser", "Simple implementation of quser.exe usingt the Windows API", 0, "<OPT:TARGET>", "10.10.10.10" )
#RegisterCommand( bofdir, "", "bofdir", "Lists a target directory using BOF.", 0, "[directory] [/s]", "C:\\Windows\\Temp" )
RegisterCommand( sa_tasklist, "", "tasklist", "This command displays a list of currently running processes on either a local or remote machine.", 0, "[hostname]", "" )
