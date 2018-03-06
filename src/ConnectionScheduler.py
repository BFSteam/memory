# AgentManager Connection Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common
import time
import os

class ConnectionScheduler(AgentManager):
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

        self.connectionLog = np.empty((0, 5))
        common.conlog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.filename = common.project.replace(
            "src", 'tmp/con_log_temp.%s.txt' % os.getpid())
        temp = open(self.filename, 'w')
        localtime = time.asctime(time.localtime(time.time()))
        print('# connectionlog')
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
        print('ag1', 'ag2', 'time', 'weight', 'type', sep=',', file=temp)
        temp.close()

    def printLog(self):
        print(self.connectionLog)

    def registerEntry(
            self,
            first=-1,
            second=-1,
            date=-1,
            weight=-1,
            cr='c',
            write=True
    ):
        """

        creates an array to stack under the log and does it

        """
        if write == False: return
        if self.connectionLog.shape[0] > 1000:
            for i in self.connectionLog:
                temp = open(self.filename, 'a')
                print(i[0], i[1], i[2], i[3], i[4],
                      sep=",", file=temp)
                temp.close()
            self.connectionLog = np.empty((0, 5))
        self.connectionLog = np.vstack((
            self.connectionLog,
            np.array([
                first,
                second,
                date,
                weight,
                cr
            ])
        ))

    def writeLog(self, path='./defCLog.csv', write=True):
        """

        saves the log from temp to path
        appends the remaining log rows
        deletes the temp

        """
        if write == False:
            print("ConnectionScheduler->writeLog called but not enabled: no file written")
            return
        for i in self.connectionLog:
            temp = open(self.filename, 'a')
            print(i[0], i[1], i[2], i[3], i[4],
                  sep=",", file=temp)
            temp.close()
        with open(path, "w") as fw, open(self.filename, 'r') as fr:
            fw.writelines(l for l in fr)
        os.remove(self.filename)
