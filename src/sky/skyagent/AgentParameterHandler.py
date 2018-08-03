from Tools import *
from agTools import *
from sky.SkyAgent import *


class AgentParameterHandler(SkyAgent):
    """

    AgentParameterHandler
    Handles the parameter of the agents at runtime

    """

    def __init__(self, number, myWorldState, agType=""):
        SkyAgent.__init__(self, number, myWorldState, agType=agType)
        self.agOperatingSets = []
        self.number = number
        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType
