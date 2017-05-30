# Agent.py
from Tools import *
from agTools import *
import graph as graph
import commonVar as common
import numpy as np


class Agent(SuperAgent):  # Agent must be the partent class of every object. Must inherit from SuperAgent

    """

    Create the parent agent
    
    Father Of All Agents
           |
    --------------------
    |                  |
    WorldAgent         SkyAgent
        |                 |
    ----------         ---------------
    |        |         |             |
    User     Source    AgentManager  ?
                            |
                       ------------
                       |
          (AgentManager)MsgScheduler
                     AMMS
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
