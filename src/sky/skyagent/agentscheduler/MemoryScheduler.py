# AgentScheduler Memory Scheduler
import csv
import os
import shutil

import commonVar as common
import numpy as np

from sky.skyagent.AgentScheduler import *
from agTools import *
from Tools import *
from usefulfunctions.useful_functions import printHeader, vprint


class MemoryScheduler(AgentScheduler):
    """

    AMMS

    """

    def __init__(self, number, myWorldState, agType):
        super().__init__(number, myWorldState, agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType

        #self.memoryLog = np.empty((0, 3 + common.memorySize))
        self.filename = common.project.replace(
            "src", 'tmp/mem_log_temp.%s.txt' % os.getpid())
        # end overload from parent class

        common.memlog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.ff = open(self.filename, 'w')
        self.w = csv.writer(self.ff)
        printHeader(
            self.w,
            firstline=['# memorylog'],
            lastline=["agent", "time", "state", "spreadstate"] +
            ["news" + str(i) for i in range(common.memorySize)])

    def printLog(self):
        print(self.messageLog)

    def updateLog(self):
        for node in range(len(common.G.nodes())):
            e = np.empty([0])
            e = np.append(e, common.G.node[node]['agent'].number)
            e = np.append(e, common.cycle)

            # old block used to distinguish between users and sources
            #
            #if (common.G.node[node]['agent'].number < common.N_SOURCES):
            #    e = np.append(e, "x")
            #else:
            #
            # end old block

            if (common.G.node[node]['agent'].active):
                e = np.append(e, "u")
            else:
                e = np.append(e, "d")
            e = np.append(e, common.G.node[node]['agent'].spreadState)
            e = np.append(e, [
                x for x in list(common.G.node[node]['agent'].database.keys())
            ])
            for i in range(4 + common.memorySize - e.shape[0]):
                e = np.append(e, 0)
            self.registerEntry(e)

    def registerEntry(self, entry, write=True):
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
        self.w.writerow(entry)

    #
    # DEPRECATING
    #
    def writeLog(self, path='./defMLog.csv', write=True):
        self.ff.close()
        if write == False:
            vprint(
                "MemoryScheduler -> writeLog called but not enabled: no file written"
            )
            os.remove(self.filename)
            return

        shutil.copy(self.filename, path)
        vprint("MemoryScheduler -> writeLog file written at", path)
        os.remove(self.filename)
        vprint("MemoryScheduler -> writeLog tmp file", self.filename,
               "removed")
