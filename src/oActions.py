import binascii
import csv
import os
import time
    
import commonVar as common
import graph as graph
import networkx as nx

from Tools import *
from usefulFunctions import worldAgentStringsizer, singleNewsStringsizer, printHeader
from world.WorldAgent import *

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

        path = common.project.replace("src", "log/graph" + str(common.localtime) + ".gml")
        nx.write_gml(common.G, path, stringizer=worldAgentStringsizer)
        print("saved", path)

        #path = common.project.replace("src", "log/graphN" + str(common.localtime) + ".gml")
        #nx.write_gml(common.G, path, stringizer=singleNewsStringsizer)
        #print("saved", path)

        path = common.project.replace("src", "log/connectionLog" + str(common.localtime) + ".csv")
        common.conlog.writeLog(path=path, write=common.writeConnections)

        path = common.project.replace("src", "log/messageLog" + str(common.localtime) + ".csv")
        common.msglog.writeLog(path=path, write=common.writeMessages)

        path = common.project.replace("src", "log/memoryLog" + str(common.localtime) + ".csv")
        common.memlog.writeLog(path=path, write=common.writeMemories)

        path = common.project.replace("src", "log/degree_distr" + str(common.localtime) + ".csv")
        with open(path, "w") as ff:
            w = csv.writer(ff)
            printHeader(w, firstline=['#degree distribution'], lastline=['node', 'degree'])
            for key, val in dict(common.G.degree()).items():
                w.writerow([key, val])

        path = common.project.replace("src", "log/clustering" + str(common.localtime) + ".csv")
        clus = nx.clustering(common.G)
        with open(path, "w") as ff:
            w = csv.writer(ff)
            printHeader(w, firstline=['#clustering per node'], lastline=['node', 'clustering coeff'])
            for key, val in clus.items():
                w.writerow([key, val])

        path = common.project.replace("src", "log/diameter" + str(common.localtime) + ".csv")
        diam = nx.diameter(max(nx.connected_component_subgraphs(common.G), key=len))
        with open(path, "w") as ff:
            w = csv.writer(ff)
            printHeader(w, firstline=['#diameter'], lastline=['diameter', 'memsize'])
            w.writerow([diam, common.memorySize])
