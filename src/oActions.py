from Tools import *
from Agent import *
import graph as graph


def do1b(address): #visualizeNet in observerActions.txt

    #basic action to visualize the networkX output
    graph.openClearNetworkXdisplay()
    graph.drawGraph()


def do2a(address, cycle): # ask_all in observerActions.txt
    self = address  # if necessary

    # ask each agent, without parameters

    print("Time = ", cycle)
    # askEachAgentInCollection(address.modelSwarm.getAgentList(),Agent.reportPosition)


def do2b(address, cycle): # ask_one in observerActions.txt
    self = address  # if necessary

    # ask a single agent, without parameters
    print("Time = ", cycle, "ask first agent to report position")
    if address.modelSwarm.getAgentList() != []:
        print('ciao')
        #askAgent(address.modelSwarm.getAgentList()[0], Agent.reportPosition)

"""             
def otherSubSteps(subStep, address):
    return False
"""
