# AgentManager
from Tools import *
from agTools import *
from SkyAgent import *


class AgentManager(SkyAgent):
    """

    AgentManager
    Class of all the managers for the agents

    """

    def __init__(self, number, myWorldState, agType=""):
        SkyAgent.__init__(self, number, myWorldState, agType=agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType
