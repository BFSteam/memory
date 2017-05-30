from Tools import *
from Agent import *
import graph as graph
import commonVar as common
import networkx as nx
from networkx.convert import to_dict_of_dicts
import pandas as pd
import time


def do1b(address):  #visualizeNet in observerActions.txt

    #basic action to visualize the networkX output
    graph.openClearNetworkXdisplay()
    graph.drawGraph()


def do2a(address, cycle):  # ask_all in observerActions.txt
    self = address  # if necessary
    # ask each agent, without parameters
    print("Time = ", cycle)

def do2b(address, cycle):  # ask_one in observerActions.txt
    if cycle == address.nCycles:
        start_time = time.time()
        path1='/home/nik/memory/log/edgelist.edges'
        path2='/home/nik/memory/log/adj.csv'
        print("saving", path1)
        nx.write_weighted_edgelist(common.G, path1, encoding='UTF-8', delimiter=',')
        print("done")
        print("saving", path1)
        nx.write_multiline_adjlist(common.G, path=path2, delimiter=',', encoding='UTF-8')
        print("done")
        print("--- %s seconds ---" % (time.time() - start_time))
