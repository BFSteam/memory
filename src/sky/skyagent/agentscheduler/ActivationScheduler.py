# AgentScheduler Activation Scheduler
import csv
import os
import shutil

import commonVar as common
import numpy as np

from sky.skyagent.AgentScheduler import *
from agTools import *
from Tools import *
from usefulFunctions import printHeader, vprint


class ActivationScheduler(AgentScheduler):
    """

    AMMS

    """

    def __init__(self, number, myWorldState, agType=""):
        AgentScheduler.__init__(
            self, number, myWorldState, agType=agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType

        #self.connectionLog = np.empty((0, 5))
        common.actlog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.filename = common.project.replace(
            "src", 'tmp/act_log_temp.%s.txt' % os.getpid())
        self.ff = open(self.filename, 'w')
        self.w = csv.writer(self.ff)
        printHeader(self.w, firstline=['#activationlog'],
                    lastline=['agent', 'time', 'type', 'dtime'])

    def registerEntry(
            self,
            agent=-1,
            date=-1,
            atype='c',
            atime=-1,
            write=True
    ):
        """

        creates an array to stack under the log and does it

        """
        if write == False:
            return
        self.w.writerow([agent,
                         date,
                         atype,
                         atime])

    def writeLog(self, path='./defALog.csv', write=True):
        """

        saves the log from temp to path
        appends the remaining log rows
        deletes the temp

        """
        self.ff.close()
        if write == False:
            vprint(
                "ActivationScheduler -> writeLog called but not enabled: no file written")
            os.remove(self.filename)
            return

        shutil.copy(self.filename, path)
        vprint("ActivationScheduler -> writeLog file written at", path)
        os.remove(self.filename)
        vprint(
            "ActivationScheduler -> writeLog tmp file",
            self.filename,
            "removed")
