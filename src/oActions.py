from Tools import *
from WorldAgent import *
import graph as graph
import commonVar as common
import networkx as nx
import time
import os
import csv
    
from usefulFunctions import worldAgentStringsizer, singleNewsStringsizer


def do1b(address):  # visualizeNet in observerActions.txt

    # basic action to visualize the networkX output
    graph.openClearNetworkXdisplay()
    graph.drawGraph()


def do2a(address, cycle):  # ask_all in observerActions.txt
    self = address  # if necessary
    # ask each agent, without parameters
    #if cycle % 25 == 0 :
    #    print("Time =", cycle)
    common.memlog.updateLog()


def do2b(address, cycle):  # ask_one in observerActions.txt
    """

    Used to save data periodicaly or at a certain time step

    """

    if cycle == address.nCycles:
        if not os.path.exists(common.project.replace("src", "log")):
            os.makedirs(common.project.replace("src", "log"))

        #path = common.project.replace("src", "log/graph.gml")
        #nx.write_gml(common.G, path, stringizer=worldAgentStringsizer)
        #print("saved", path)

        #path = common.project.replace("src", "log/graphN.gml")
        #nx.write_gml(common.G, path, stringizer=singleNewsStringsizer)
        #print("saved", path)

        path = common.project.replace("src", "log/connectionLog.csv")
        common.conlog.writeLog(path=path, write=common.writeConnectons)
        print("saved", path)

        path = common.project.replace("src", "log/messageLog.csv")
        common.msglog.writeLog(path=path, write=common.writeMessages)
        print("saved", path)

        path = common.project.replace("src", "log/memoryLog.csv")
        common.memlog.writeLog(path=path, write=common.writeMemories)
        print("saved", path)

        path = common.project.replace("src", "log/degree_distr.csv")        
        w = csv.writer(open(path, "w"))
        w.writerow(["#header"])
        w.writerow(["node", "degree"])
        for key, val in dict(common.G.degree()).items():
            w.writerow([key, val])

        path = common.project.replace("src", "log/clustering.csv")
        clus = nx.clustering(common.G)
        w = csv.writer(open(path, "w"))
        w.writerow(["#header"])
        w.writerow(["node", "clustering coeff"])
        for key, val in clus.items():
            w.writerow([key, val])

        path = common.project.replace("src", "log/diameter.csv")
        diam = nx.diameter(max(nx.connected_component_subgraphs(common.G), key=len))
        w = csv.writer(open(path, "w"))
        w.writerow(["#header"])
        w.writerow([diam])
