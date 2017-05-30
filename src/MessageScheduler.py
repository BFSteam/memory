# AgentManager Message Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np


class MessageScheduler(AgentManager):
    """

    AMMS

    """

    def __init__(self, number, myWorldState, agType=""):
        AgentManager.__init__(self, number, myWorldState, agType=agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType

        self.msgLog = np.zeros([8])

    def printLog(self):
        print(self.msgLog)

    def addToLog(self, arr):
        """

        stacks an array under the log

        """

        if arr.shape[0] != 8:
            return False
        if any(self.msgLog) is False:
            self.msgLog = arr
            return True
        else:
            self.msgLog = np.vstack((self.msgLog, a))
            return True

    def registerEntry(self, id_src=-1, date=-1, sender=-1, reciver=-1, id_new='null', date_sender=-1, date_reciver=-1, diffusion='a'):
        """

        creates an array to stack under the log and does it

        self.msgLog = np.vstack((
            self.msgLog,
            np.array([
                id_src,
                date,
                id_new,
                sender,
                reciver,
                date_sender,
                date_reciver,
                diffusion
            ])
        ))

        """

        self.msgLog = np.vstack((
            self.msgLog,
            np.array([
                id_src,
                date,
                id_new,
                sender,
                reciver,
                date_sender,
                date_reciver,
                diffusion
            ])
        ))
