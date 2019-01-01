# AgentScheduler Spread State Scheduler
import csv
import os
import shutil

import commonVar as common
import numpy as np
from termcolor import colored
from sky.skyagent.AgentScheduler import *
from agTools import *
from Tools import *

from coloroutput import DEBUG_LABEL, LOG_LABEL, OK_LABEL, INPUT_LABEL, WARNING_MSG, ERROR_MSG
from usefulfunctions.useful_functions import printHeader, vprint


class SreadStateScheduler(AgentScheduler):
    """

    SSS
    This scheduler is called every time the spread state of an agent 
    changes

    """

    def __init__(self, number, myWorldState, agType, *args, **kwargs):
        super().__init__(number, myWorldState, agType, *args, **kwargs)
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
            "src", 'tmp/sp_st__log_temp.%s.txt' % os.getpid())
        self.ff = open(self.filename, 'w')
        self.w = csv.writer(self.ff)
        printHeader(
            self.w,
            firstline=['#spreadStatelog'],
            lastline=['time', 'agent', 'state1', 'state2'])

    def registerEntry(self,
                      agent=-1,
                      date=-1,
                      state1='x',
                      state2='y',
                      write=True):
        """

        creates an array to stack under the log and does it

        """
        if write == False:
            return
        self.w.writerow([date, agent, state1, state2])

    def writeLog(self, path='./defSLog.csv', write=True):
        """

        saves the log from temp to path
        appends the remaining log rows
        deletes the temp

        """
        self.ff.close()
        if write == False:
            vprint(
                WARNING_MSG +
                "SpreadStateScheduler -> writeLog called but not enabled: no file written"
            )
            os.remove(self.filename)
            return

        shutil.copy(self.filename, path)
        vprint(
            LOG_LABEL + "SpreadStateScheduler -> writeLog file written at",
            path,
        )
        os.remove(self.filename)
        vprint(LOG_LABEL + "SpreadStateScheduler -> writeLog tmp file",
               self.filename, "removed")
