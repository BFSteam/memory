# Agent.py
from Tools import *
from agTools import *
import graph as graph
import commonVar as common
import numpy as np


class Agent(SuperAgent):  # Agent must be the partent class of every object. Must inherit from SuperAgent

    """

    Create the parent agent

    Def. constructor:
    class Agent(SuperAgent):
        def __init__(self, number,myWorldState, xPos, yPos, lX =-20,rX=19, bY=-20,tY=19, agType="")

    """

    def __init__(self, number, myWorldState, agType=""):
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType

        self.state = np.array([random.random() for i in range(common.dim)])
        self.state = self.state / self.state.sum()

        if graph.getGraph() == 0:
            graph.createGraph()  # if first agent create the graph
        common.G.add_node(self.number, agent=self)  # adds himself
        if common.cycle == 1:  # create link only if you are only at the first step of the clock and if you are the last user
            if len(common.G.nodes()) == common.N_AGENTS:
                graph.initializeEdges()  # if last creates edges

        self.active = True
        self.databaseCols = ['id-n',
                             'new',
                             'id-source',
                             'date-creation',
                             'relevance',
                             'id-send',
                             'date-send',
                             'id-recive',
                             'date-recive']
        self.database = {}
        print("agent", self.agType, "#", self.number, "has been created")

    def getGraph(self):
        return common.G

    def hasNews(self, id_source=0, date=1):
        pass
