import os
import random
import warnings

import commonVar as common
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


warnings.filterwarnings("ignore", ".*GUI is implemented.*")
import usefulFunctions as uf
#import seaborn as sns


def createGraph():
    global colors, pos

    # graph undirected to set weight specify them as a parameter creating the
    # edges
    common.G = nx.Graph()
    colors = {}
    pos = {}
    common.G_labels = {}
    common.G_edge_labels = {}  # copy the address of the labels of the edges


def initializeEdges():
    """

    random initialization of edges

    """

    for i in list(common.G.nodes()):
        for j in list(common.G.nodes()):
            if j > i:
                if i < common.N_SOURCES and j < common.N_SOURCES:
                    pass
                elif i >= common.N_SOURCES and j >= common.N_SOURCES:
                    if random.random() < common.P_a:
                        common.G.add_edge(
                            i, j, weight=0.3 + 0.7 * random.random())
                        common.conlog.registerEntry(
                            first=i,
                            second=j,
                            date=common.cycle,
                            weight=common.G[i][j]['weight'],
                            cr='a',
                            write=common.writeConnections
                        )
                else:
                    if random.random() < common.P_s:
                        common.G.add_edge(
                            i, j, weight=0.3 + 0.7 * random.random())
                        common.conlog.registerEntry(
                            first=i,
                            second=j,
                            date=common.cycle,
                            weight=common.G[i][j]['weight'],
                            cr='a',
                            write=common.writeConnections
                        )


# using networkX and matplotlib case
def closeNetworkXdisplay():
    plt.close()


def openClearNetworkXdisplay():
    if common.graphicStatus == "PythonViaTerminal":
        plt.ion()
    # plt.clf()


def clearNetworkXdisplay():
    plt.clf()


def getGraph():
    """

    returns the graph if exists
    else returns zero

    """

    try:
        return common.G
    except:
        return 0


def drawGraph(n=True, e=True, l=True, clrs='state', static=True):

    clearNetworkXdisplay()
    c = []
    if clrs == 'state':  # draw colors thinking of state
        print(common.G.node[0]['agent'].hasNews(id_source=0, date=1))
        
        for i in list(common.G.nodes()):
            if common.G.node[i]['agent'].hasNews(id_source=0, date=1) is True:
                c.append('#ffa500')
                continue
            elif common.G.node[i]['agent'].hasNews(id_source=1, date=1) is True:
                c.append('#ff748c')
                continue
            elif common.G.node[i]['agent'].hasNews(id_source=2, date=1) is True:
                c.append('#38ffc8')
                continue
            else:
                if common.G.nodes()[i]['agent'].number < common.N_SOURCES:
                    c.append('red')
                    continue
                else:
                    if common.G.nodes[i]['agent'].active is True:
                        c.append('blue')
                        continue
                    else:
                        c.append('grey')
                        continue

    node_size = []
    for i in list(common.G.nodes()):
        if common.G.nodes()[i]['agent'].number < common.N_SOURCES:
            node_size.append(100)
        else:
            node_size.append(60)
    pos = nx.spring_layout(common.G)
    if n is True:  # draw nodes
        nx.draw_networkx_nodes(
            common.G, pos, node_size=node_size, node_color=c)

    if e is True:  # draw edges
        nx.draw_networkx_edges(common.G, pos, edge_color='black')

    if l is True:  # draw labels
        nx.draw_networkx_labels(common.G, pos, font_size=8)

    plt.title(
        'seed:'+ str(common.SEED) +
        'u:' + str(common.N_USERS) +
        's:' + str(common.N_SOURCES) +
        'av.deg.:' + str(common.averageDegree) +
        't:' + str(common.cycle) +"/" + str(common.N_CYCLES)
    )
    # plt.show()  # show plot
    if not os.path.exists(common.project.replace("src", "log")):
        os.makedirs(common.project.replace("src", "log"))
    plotpath = common.project.replace(
        "src", "log/plot-%04d.pdf" % common.cycle)
    plt.savefig(plotpath)
    print("saved plot:", plotpath)
    if common.graphicStatus == "PythonViaTerminal":
        plt.pause(0.1)
    # to show the sequence of the shown images in absence of pauses
