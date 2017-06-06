# AgentManager Memory Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common
import time
import os


class MemoryScheduler(AgentManager):
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

        self.memoryLog = np.empty((0, 2 + common.memorySize))
        print(self.memoryLog)

        common.memlog = self
        self.filename = common.project + '/mem_log_temp.%s.txt' % os.getpid()
        temp = open(self.filename, 'w')
        localtime = time.asctime(time.localtime(time.time()))
        print('# memorylog')
        print('#', localtime, file=temp)
        print('#simulation with:', file=temp)
        print('#N_AGENTS', common.N_AGENTS, file=temp)
        print('#N_SOURCES', common.N_SOURCES, file=temp)
        print('#P_a', common.P_a, file=temp)
        print('#P_s', common.P_s, file=temp)
        print('#dim', common.dim, file=temp)
        print('#memorySize', common.memorySize, file=temp)
        print("agent", "time", sep=',', end="", file=temp)
        for i in range(common.memorySize):
            print(",", sep="", end="", file=temp)
            print("news", str(i), sep="", end="", file=temp)
        print(" ", file=temp)
        temp.close()

    def printLog(self):
        print(self.messageLog)

    def updateLog(self):
        for node in range(len(common.G.nodes())):
            e = np.empty([0])
            e = np.append(e, common.G.node[node]['agent'].number)
            e = np.append(e, common.cycle)
            e = np.append(
                e, [x.decode('utf-8') for x in list(common.G.node[node]['agent'].database.keys())])
            for i in range(2 + common.memorySize - e.shape[0]):
                e = np.append(e, 0)
            self.registerEntry(e)

    def registerEntry(
            self,
            entry
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
        if self.memoryLog.shape[0] > 1000:
            for i in self.memoryLog:
                temp = open(self.filename, 'a')
                print(*i, sep=",", file=temp)
                temp.close()
            self.memoryLog = np.empty((0, 2 + common.memorySize))

        tarr = np.empty([0])
        for i in range(2 + common.memorySize):
            tarr = np.append(tarr, entry[i])
        self.memoryLog = np.vstack((
            self.memoryLog,
            tarr
        ))

    def writeLog(self, path='./defMLog.csv'):

        # try to guess extension
        for i in self.memoryLog:
            temp = open(self.filename, 'a')
            print(*i, sep=",", file=temp)
            temp.close()

        with open(path, "w") as fw, open(self.filename, 'r') as fr:
            fw.writelines(l for l in fr)
        os.remove(self.filename)
