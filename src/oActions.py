from Tools import *
from WorldAgent import *
import graph as graph
import commonVar as common
import networkx as nx
import time
import os
from usefulFunctions import worldAgentStringsizer, singleNewsStringsizer


def do1b(address):  # visualizeNet in observerActions.txt

    # basic action to visualize the networkX output
    graph.openClearNetworkXdisplay()
    graph.drawGraph()


def do2a(address, cycle):  # ask_all in observerActions.txt
    self = address  # if necessary
    # ask each agent, without parameters
    print("Time = ", cycle)
    common.memlog.updateLog()


def do2b(address, cycle):  # ask_one in observerActions.txt
    """

    Used to save data periodicaly or at a certain time step

    """

    if cycle == address.nCycles:
        if not os.path.exists(common.project.replace("src", "log")):
            os.makedirs(common.project.replace("src", "log"))
        path = common.project.replace("src", "log/graph.gml")
        nx.write_gml(common.G, path, stringizer=worldAgentStringsizer)
        print("saved", path)
        path = common.project.replace("src", "log/graphN.gml")
        nx.write_gml(common.G, path, stringizer=singleNewsStringsizer)
        print("saved", path)
        path = common.project.replace("src", "log/connectionLog.csv")
        common.conlog.writeLog(path=path)
        print("saved", path)
        path = common.project.replace("src", "log/messageLog.csv")
        common.msglog.writeLog(path=path)
        print("saved", path)
        path = common.project.replace("src", "log/memoryLog.csv")
        common.memlog.writeLog(path=path)
        print("saved", path)
