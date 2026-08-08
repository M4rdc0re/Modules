from vaelix_host import Agent, RegisterCallback

def new_agent( agentID ):
    agent  : Agent  = None
    agent  = Agent( agentID )

    if agent.OSArch.startswith(agent.ProcessArch) is False:
        TaskID = agent.ConsoleWrite( agent.CONSOLE_TASK, f"migrating to x64" )
        agent.Command(TaskID, 'shellcode spawn x64 /tmp/agent.x64.bin')

RegisterCallback(new_agent)
