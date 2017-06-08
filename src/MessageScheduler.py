# AgentManager Message Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common
import time
import os


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

        self.msgLog = np.empty((0, 7))
        print(self.msgLog)
        common.msglog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.filename = common.project.replace(
            "src", 'tmp/msg_log_temp.%s.txt' % os.getpid())
        temp = open(self.filename, 'w')
        localtime = time.asctime(time.localtime(time.time()))
        print('# messagelog')
        print('#', localtime, file=temp)
        print('#simulation with:', file=temp)
        print('#SEED', common.SEED, file=temp)
        print('#N_AGENTS', common.N_AGENTS, file=temp)
        print('#N_USERS', common.N_USERS, file=temp)
        print('#N_SOURCES', common.N_SOURCES, file=temp)
        print('#P_a', common.P_a, file=temp)
        print('#P_s', common.P_s, file=temp)
        print('#dim', common.dim, file=temp)
        print('#time', common.N_CYCLES, file=temp)
        print('#memorySize', common.memorySize, file=temp)
        print("source", "timec", "news", "ag1", "ag2",
              "time", "type", sep=',', file=temp)
        temp.close()

    def printLog(self):
        print(self.msgLog)

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
        if self.msgLog.shape[0] > 1000:
            for i in self.msgLog:
                temp = open(self.filename, 'a')
                print(i[0], i[1], i[2], i[3], i[4], i[5], i[6],
                      sep=",", file=temp)
                temp.close()
            self.msgLog = np.empty((0, 7))
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

    def writeLog(self, path='./defMLog.csv'):

        # try to guess extension
        for i in self.msgLog:
            temp = open(self.filename, 'a')
            print(i[0], i[1], i[2], i[3], i[4], i[5], i[6],
                  sep=",", file=temp)
            temp.close()
        with open(path, "w") as fw, open(self.filename, 'r') as fr:
            fw.writelines(l for l in fr)
        os.remove(self.filename)
