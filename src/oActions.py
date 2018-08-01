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
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        #
        # GML's
        #
        #-------------------------------------------------------------
        #
        # GML
        #
        path = common.project.replace(
            "src",
            "log/graph" + str(common.localtime) + ".gml")
        nx.write_gml(common.G, path, stringizer=worldAgentStringsizer)
        print("saved", path)
        #-------------------------------------------------------------
        #
        # GML different stringsizer
        #
        #path = common.project.replace(
        #    "src",
        #    "log/graphN" + str(common.localtime) + ".gml")
        #nx.write_gml(common.G, path, stringizer=singleNewsStringsizer)
        #print("saved", path)
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        #
        # AGENT MANAGERS
        #
        #-------------------------------------------------------------
        #
        # CONNECTION LOG
        #
        path = common.project.replace(
            "src",
            "log/connectionLog" + str(common.localtime) + ".csv")
        common.conlog.writeLog(
            path=path,
            write=common.writeConnections)
        #-------------------------------------------------------------
        #
        # MESSAGE LOG 
        #
        path = common.project.replace(
            "src",
            "log/messageLog" + str(common.localtime) + ".csv")
        common.msglog.writeLog(
            path=path,
            write=common.writeMessages)
        #-------------------------------------------------------------
        #
        # MEMORY LOG
        #
        path = common.project.replace(
            "src",
            "log/memoryLog" + str(common.localtime) + ".csv")
        common.memlog.writeLog(
            path=path,
            write=common.writeMemories)
        #-------------------------------------------------------------
        #
        # ACTIVATION LOG
        #
        path = common.project.replace(
            "src",
            "log/activationLog" + str(common.localtime) + ".csv")
        common.actlog.writeLog(
            path=path,
            write=common.writeMemories)
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        #
        # NETWORK MEASURES
        #
        #-------------------------------------------------------------
        #
        # DEGREE DISTRIBUTION
        #
        path = common.project.replace(
            "src",
            "log/degree_distr" + str(common.localtime) + ".csv")
        with open(path, "w") as ff:
            w = csv.writer(ff)
            printHeader(w,
                        firstline=['#degree distribution'],
                        lastline=['node', 'degree'])
            for key, val in dict(common.G.degree()).items():
                w.writerow([key, val])
        #-------------------------------------------------------------
        #
        # CLUSTERING COEFFICIENT
        #
        path = common.project.replace(
            "src",
            "log/clustering" + str(common.localtime) + ".csv")
        clus = nx.clustering(common.G)
        with open(path, "w") as ff:
            w = csv.writer(ff)
            printHeader(w,
                        firstline=['#clustering per node'],
                        lastline=['node', 'clustering coeff'])
            for key, val in clus.items():
                w.writerow([key, val])
        #-------------------------------------------------------------
        #
        # DIAMETER
        #
        path = common.project.replace(
            "src",
            "log/diameter" + str(common.localtime) + ".csv")
        diam = nx.diameter(
            max(nx.connected_component_subgraphs(common.G), key=len))
        with open(path, "w") as ff:
            w = csv.writer(ff)
            printHeader(w,
                        firstline=['#diameter'],
                        lastline=['diameter', 'memsize'])
            w.writerow([diam, common.memorySize])
        #-------------------------------------------------------------
        #
        # K - CORE
        #
        path = common.project.replace(
            "src",
            "log/kcore" + str(common.localtime) + ".csv")
        common.G.remove_edges_from(nx.selfloop_edges(common.G))
        kcore = nx.core_number(common.G)
        with open(path, "w") as ff:
            w = csv.writer(ff)
            printHeader(w,
                        firstline=['#k-core'],
                        lastline=['node', 'k-core'])
            for key, val in dict(kcore).items():
                w.writerow([key, val])
        #-------------------------------------------------------------
        try:
            from pybeep.pybeep import PyVibrate, PyBeep
            PyBeep().beep()
        except:
             pass

## TODO implement single string replacement
