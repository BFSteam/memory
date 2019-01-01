# AgentScheduler Activation Scheduler
import csv
import os
import shutil

import commonVar as common
import numpy as np
from termcolor import colored
from sky.skyagent.AgentScheduler import *
from agTools import *
from Tools import *
from usefulfunctions.useful_functions import printHeader, vprint


class ActivationScheduler(AgentScheduler):
    """

    AMMS
    This scheduler is called every time the state of an agent changes
    from active to inactive and vice versa

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
            "src", 'tmp/act_log_temp.%s.txt' % os.getpid())
        self.ff = open(self.filename, 'w')
        self.writer = csv.writer(self.ff)
        self.chunk = []
        self.active = common.writeActivations
        printHeader(
            self.writer,
            firstline=['#activationlog'],
            lastline=['agent', 'time', 'type', 'dtime'])

    def registerEntry(self, agent=-1, date=-1, atype='c', atime=-1,
                      write=True):
        """

        creates an array to stack under the log and does it

        """
        if write == False:
            return
        self.register_entry_in_chunk([agent, date, atype, atime])

    #
    # DEPRECATING
    #
    def writeLog(self, path='./defALog.csv', write=True):
        """

        saves the log from temp to path
        appends the remaining log rows
        deletes the temp

        """
        self.ff.close()
        if write == False:
            vprint(
                colored(
                    "ActivationScheduler -> writeLog called but not enabled: no file written",
                    "yellow"))
            os.remove(self.filename)
            return

        shutil.copy(self.filename, path)
        vprint(
            self.agType + "ActivationScheduler -> writeLog file written at",
            path,
        )
        os.remove(self.filename)
        vprint("ActivationScheduler -> writeLog tmp file", self.filename,
               "removed")
