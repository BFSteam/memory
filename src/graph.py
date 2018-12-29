import csv
import os
import random
import warnings

import commonVar as common
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

warnings.filterwarnings("ignore", ".*GUI is implemented.*")
import usefulfunctions.useful_functions as uf

#import seaborn as sns


def create_graph():
    """
    Creates the graph and dictionaries to display colors, pos...
    Stores the graph in commonVar module
    """
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

    # read adjacency matrix from file
    if common.networkfilepath != "":
        with open(common.networkfilepath, "r") as adj:
            reader = csv.reader(adj, delimiter=",")
            for row in reader:
                if row == []: continue

                # try to read all the columns
                try:
                    first = int(row[0])
                    second = int(row[1])
                    weight = int(row[2])
                except:
                    first = int(row[0])
                    second = int(row[1])
                    weight = np.random.random_sample()

                # create edge on the graph and register entry in the log file
                common.G.add_edge(first, second, weight=weight)
                common.conlog.registerEntry(
                    first=first,
                    second=second,
                    date=common.cycle,
                    weight=weight,
                    cr='a',
                    write=common.writeConnections)

        # new untested block
        #
        if -1 not in common.source_index and common.source_index[
                0] < common.N_AGENTS:
            common.G.node[common.source_index[0]]['agent'].spreadState = 'i'
        else:
            common.G.node[np.random.randint(
                0, common.N_AGENTS)]['agent'].spreadState = 'i'
        #
        # end block

        # === this block is gonna be deprecated soon ======================
        #print('old block: source agent swapped: deprecating in the future')
        #tempindex = np.random.randint(0, common.N_AGENTS)
        #if -1 not in common.source_index and common.source_index[
        #        0] < common.N_AGENTS:
        #    tempindex = common.source_index[0]
        #tempagent = common.G.node[0]['agent']
        #common.G.node[0]['agent'] = common.G.node[tempindex]['agent']
        #common.G.node[tempindex]['agent'] = tempagent
        # === end block ===================================================

    # ================================================================
    # old code used to creating random network
    # may be dismissed in future
    # not used if adjacency matrix is passed
    else:
        print('old block: random network: deprecating in the future')
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
                                write=common.writeConnections)
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
                                    write=common.writeConnections)
    # ================================================================


# using networkX and matplotlib case
def closeNetworkXdisplay():
    plt.close()


def openClearNetworkXdisplay():
    if common.graphicStatus == "PythonViaTerminal":
        plt.ion()
    # plt.clf()


def clearNetworkXdisplay():
    plt.clf()


def get_graph():
    """

    returns the graph if exists
    else returns zero

    """

    try:
        return common.G
    except BaseException:
        return 0


def drawGraph(n=True, e=True, l=True, clrs='state', static=True, shape=True):
    state_color_dict = {  # light active, dark inactive
        's': {  # sane -> green
            'active': '#008000',
            'inactive': '#004000'
        },
        'i': {  # infective -> red
            'active': '#FF0000',
            'inactive': '#990000'
        },
        'r': {  # recovery -> blue
            'active': '#0000FF',
            'inactive': '#000099'
        }
    }
    clearNetworkXdisplay()
    c = []
    if clrs == 'state':  # draw colors thinking of state
        for i in list(common.G.nodes()):
            try:
                temp_state = 'active' if (
                    common.G.node[i]['agent'].active is True) else 'inactive'
                c.append(state_color_dict[common.G.node[i]['agent'].
                                          spreadState][temp_state])
            except:
                c.append('#808080')
        #print(common.G.node[0]['agent'].has_news_in_database(
        #    id_source=0, date=1))
        #for i in list(common.G.nodes()):
        #    if common.G.node[i]['agent'].has_news_in_database(
        #            id_source=0, date=1) is True:
        #        c.append('#ffa500')
        #        continue
        #    elif common.G.node[i]['agent'].has_news_in_database(
        #            id_source=1, date=1) is True:
        #        c.append('#ff748c')
        #        continue
        #    elif common.G.node[i]['agent'].has_news_in_database(
        #            id_source=2, date=1) is True:
        #        c.append('#38ffc8')
        #        continue
        #    else:
        #        if common.G.nodes()[i]['agent'].spreadState == "s":
        #            c.append('red')
        #            continue
        #        else:
        #            if common.G.nodes[i]['agent'].active is True:
        #                c.append('blue')
        #                continue
        #            else:
        #                c.append('grey')
        #                continue

    node_size = []
    for i in list(common.G.nodes()):
        if common.G.nodes()[i]['agent'].spreadState == "i":
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

    plt.title('seed:' + str(common.SEED) + 'u:' + str(common.N_USERS) + 's:' +
              str(common.N_SOURCES) + 'av.deg.:' + str(common.averageDegree) +
              't:' + str(common.cycle) + "/" + str(common.N_CYCLES))
    # plt.show()  # show plot
    if not os.path.exists(common.project.replace("src", "log")):
        os.makedirs(common.project.replace("src", "log"))
    plotpath = common.project.replace("src",
                                      "log/plot-%04d.pdf" % common.cycle)
    plt.savefig(plotpath)
    print("saved plot:", plotpath)
    if common.graphicStatus == "PythonViaTerminal":
        plt.pause(0.1)
    # to show the sequence of the shown images in absence of pauses
