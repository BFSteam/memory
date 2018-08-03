# Agent.py
import numpy as np

import commonVar as common
import graph as graph

from agTools import *
from Tools import *


class Agent(
        SuperAgent):  # Agent must be the partent class of every object. Must inherit from SuperAgent

    """

    Create the parent agent

    Father Of All Agents
           |
    --------------------
    |                  |
    WorldAgent         SkyAgent
        |                 |
    ----------         -------------------------------
    |        |         |                             |
    User     Source    AgentManager(AgentScheduler)  AgentParameterHandler
                            |                             |
                       -------------------              ----------
                       |                 |              |        |
          (AgentManager)MsgScheduler     ConnScheduler  ?        ?
                     AMMS                    AMCS

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
