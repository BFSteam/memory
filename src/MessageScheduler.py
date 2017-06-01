# AgentManager Message Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common


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

        self.msgLog = np.zeros([7])

        common.log = self

    def printLog(self):
        print(self.msgLog)

    def addToLog(self, arr):
        """

        stacks an array under the log

        """

        if arr.shape[0] != 7:
            return False
        if any(self.msgLog) is False:
            self.msgLog = arr
            return True
        else:
            self.msgLog = np.vstack((self.msgLog))
            return True

    def registerEntry(
            self,
            id_src=-1,
            date_creation=-1,
            sender=-1,
            reciver=-1,
            id_new='null',
            date=-1,
            diffusion='n'
    ):
        """

        creates an array to stack under the log and does it

        self.msgLog = np.vstack((
            self.msgLog,
            np.array([
                id_src,
                date_creation,
                id_new,
                sender,
                reciver,
                date,
                diffusion
            ])
        ))

        """
        self.msgLog = np.vstack((
            self.msgLog,
            np.array([
                id_src,
                date_creation,
                id_new,
                sender,
                reciver,
                date,
                diffusion
            ])
        ))

    def writeLog(self, readable=True):
        f = open('/home/nik/memory/log/log.txt', 'w')
        if readable is True:
            for i in self.msgLog:
                f.write("News ")
                f.write(str(i[2]))
                f.write(" created by source ")
                f.write(str(i[0]))
                f.write(" at cycle ")
                f.write(str(i[1]))
            if i[6] == 'a':
                f.write(" diffused actively from ")
                f.write(str(i[3]))
                f.write(" to ")
                f.write(str(i[4]))
                f.write(" at cycle ")
                f.write(str(i[5]))
            elif i[6] == 'p':
                f.write(" diffused passively from ")
                f.write(str(i[3]))
                f.write(" to ")
                f.write(str(i[4]))
                f.write(" at cycle ")
                f.write(str(i[5]))
            f.write("\n")
        else:
            for i in self.msgLog:
                f.write(str(i))
                f.write('\n')
        print("saved log")
