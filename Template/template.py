from vaelix_host import Agent, RegisterCommand

def testdll(agentID, *param):
    TaskID : str    = None
    agent  : Agent  = None
    packer = Packer()

    packer.addstr("test1234")

    agent  = Agent(agentID)
    TaskID = agent.ConsoleWrite(agent.CONSOLE_TASK, "Tasked agent spawn and inject a test dll")
    
    arg = packer.getbuffer() 

    agent.DllSpawn(TaskID, "/tmp/test.dll", arg)

    return TaskID

RegisterCommand(testdll, "", "testdll", "spawn and inject test dll", 0, "", "")
