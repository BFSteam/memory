# AgentManager Memory Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common
import os
import csv
from usefulFunctions import printHeader, vprint


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

        self.memoryLog = np.empty((0, 3 + common.memorySize))

        common.memlog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.filename = common.project.replace(
            "src", 'tmp/mem_log_temp.%s.txt' % os.getpid())
        with open(self.filename, 'w') as ff:
            w = csv.writer(ff)
            printHeader(w, firstline=['# memorylog'],
                        lastline=["agent", "time", "state"] + ["news" + str(i) for i in range(common.memorySize)])

    def printLog(self):
        print(self.messageLog)

    def updateLog(self):
        for node in range(len(common.G.nodes())):
            e = np.empty([0])
            e = np.append(e, common.G.node[node]['agent'].number)
            e = np.append(e, common.cycle)
            if(common.G.node[node]['agent'].number < common.N_SOURCES):
                e = np.append(e, "x")
            else:
                if(common.G.node[node]['agent'].active):
                    e = np.append(e, "u")
                else:
                    e = np.append(e, "d")

            e = np.append(e, [x.decode('utf-8') for x in list(common.G.node[node]['agent'].database.keys())])
            for i in range(3 + common.memorySize - e.shape[0]):
                e = np.append(e, 0)
            self.registerEntry(e)

    def registerEntry(
            self,
            entry,
            write=True
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
        if write == False:
            return
        if self.memoryLog.shape[0] > 1000:
            with open(self.filename, 'a') as ff:
                w = csv.writer(ff)
                for i in self.memoryLog:
                    w.writerow(i)
                self.memoryLog = np.empty((0, 3 + common.memorySize))

        tarr = np.empty([0])
        for i in range(3 + common.memorySize):
            tarr = np.append(tarr, entry[i])
        self.memoryLog = np.vstack((
            self.memoryLog,
            tarr
        ))

    def writeLog(self, path='./defMLog.csv', write=True):

        if write == False:
            vprint("MemoryScheduler -> writeLog called but not enabled: no file written")
            os.remove(self.filename)
            return
        # try to guess extension
        with open(self.filename, 'a') as ff:
            w = csv.writer(ff)
            for i in self.memoryLog:
                w.writerow(i)

        with open(path, "w") as fw, open(self.filename, 'r') as fr:
            fw.writelines(l for l in fr)
        vprint("MemoryScheduler -> writeLog file written at", path)
        os.remove(self.filename)
        vprint("MemoryScheduler -> writeLog tmp file", self.filename, "removed")
