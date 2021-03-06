# WorldAgent.py
import random

import datastructures.database as db
from coloroutput import LOG_LABEL
from usefulfunctions.useful_functions import norm

import commonVar as common
import graph as graph
import numpy as np

from Tools import *
from agTools import *
from Agent import *


# Agent must be the partent class of every object. Must inherit from SuperAgent
class WorldAgent(Agent):
    """

    Create the parent agent

    Def. constructor:
    class Agent(SuperAgent):
        def __init__(self, number,myWorldState, xPos, yPos, lX =-20,rX=19, bY=-20,tY=19, agType="")

    The King of all the earth agents

            *
          * | *
         * \|/ *
    * * * \|O|/ * * *
     \o\o\o|O|o/o/o/
     (<><><>O<><><>)
      '==========='

    """

    def __init__(self, number, myWorldState, agType):
        super().__init__(number, myWorldState, agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType

        self.state = np.zeros([common.dim])
        self.active = True
        #self.databaseCols = [
        #    'id-n', 'new', 'id-source', 'date-creation', 'relevance',
        #    'id-send', 'date-send', 'id-recive', 'date-recive'
        #]
        self.database = db.database()
        self.spreadState = 's'
        #print(LOG_LABEL, "agent", self.agType, "#", self.number,
        #"has been created")

        # =========================================================================================
        #
        # GRAPH CREATION
        #
        if graph.get_graph() == 0:
            graph.create_graph()  # if first agent create the graph
        common.G.add_node(self.number, agent=self)  # adds himself
        # create link only if you are only at the first step of the clock
        # and if you are the last user
        if common.cycle == 1 and len(common.G.nodes()) == common.N_AGENTS:
            graph.initialize_edges()  # if last creates edges
            graph.change_s_to_i()
        #
        # =========================================================================================

    def genState(self, n=1, noise=15):
        # source state
        # inizializzato a zero
        # number of relevant topics for the source: 1, 2 or 3
        # added r number of ones and noise: the noise is 0.15 for one single
        # topic, 0.1 for 2 and 0.5 for three
        # the state is shuffled because the topics are not in a partcular
        # order. then it's normalized
        self.state = np.zeros([self.state.shape[0]])
        if n > 0:
            r = random.randint(1, n)
            for i in range(r):
                self.state[i] = 1
            for i in range(self.state.shape[0]):
                self.state[i] += (noise / r) * np.random.random_sample()
            random.shuffle(self.state)
        else:
            for i in range(self.state.shape[0]):
                self.state[i] += np.random.random_sample()
        self.state = norm(self.state)
        return self.state

    def get_graph(self):
        return common.G

    def has_news_in_database(self, id_source=0, date=1):
        pass

    def debug(self):
        print(self.number)
        print(self.database)
