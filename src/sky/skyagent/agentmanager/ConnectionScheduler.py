# AgentManager Connection Scheduler
import csv
import os
import shutil

import commonVar as common
import numpy as np

from sky.skyagent.AgentManager import *
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

        #self.connectionLog = np.empty((0, 5))
        common.conlog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.filename = common.project.replace(
            "src", 'tmp/con_log_temp.%s.txt' % os.getpid())
        self.ff = open(self.filename, 'w')
        self.w = csv.writer(self.ff)
        printHeader(self.w, firstline=['#connectionlog'],
                    lastline=['ag1', 'ag2', 'time', 'weight', 'type'])

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
        self.w.writerow([first,
                         second,
                         date,
                         weight,
                         cr])

    def writeLog(self, path='./defCLog.csv', write=True):
        """

        saves the log from temp to path
        appends the remaining log rows
        deletes the temp

        """
        self.ff.close()
        if write == False:
            vprint("ConnectionScheduler -> writeLog called but not enabled: no file written")
            os.remove(self.filename)
            return

        shutil.copy(self.filename, path)
        vprint("ConnectionScheduler -> writeLog file written at", path)
        os.remove(self.filename)
        vprint("ConnectionScheduler -> writeLog tmp file", self.filename, "removed")
