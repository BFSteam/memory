# AgentManager Connection Scheduler
import csv
import os

import commonVar as common
import numpy as np

from AgentManager import *
from agTools import *
from Tools import *
from usefulFunctions import printHeader, vprint

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
        with open(self.filename, 'w') as ff:
            w = csv.writer(ff)
            printHeader(w, firstline=['#connectionlog'],
                        lastline=['ag1', 'ag2', 'time', 'weight', 'type'])

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
            with open(self.filename, 'a') as ff: # open file ff at path self.filepath
                w = csv.writer(ff)               # open csv writer 
                for i in self.connectionLog:
                    w.writerow(i[0:5])           # write what you need -> file closes at end of with
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
            vprint("ConnectionScheduler -> writeLog called but not enabled: no file written")
            os.remove(self.filename)
            return
        with open(self.filename, 'a') as cl:
            w = csv.writer(cl)
            for i in self.connectionLog:
                w.writerow(i[0:5])

        with open(path, "w") as fw, open(self.filename, 'r') as fr:
            fw.writelines(l for l in fr)
        vprint("ConnectionScheduler -> writeLog file written at", path)
        os.remove(self.filename)
        vprint("ConnectionScheduler -> writeLog tmp file", self.filename, "removed")
