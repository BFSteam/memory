# AgentScheduler
from Tools import *
from agTools import *
from sky.SkyAgent import *


class AgentScheduler(SkyAgent):
    """

    AgentScheduler
    Class of all the Schedulers for the agents

    """

    def __init__(self, number, myWorldState, agType=""):
        super(AgentScheduler, self).__init__(
            self, number, myWorldState, agType=agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType
