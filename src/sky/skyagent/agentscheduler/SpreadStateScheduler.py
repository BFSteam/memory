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


class SpreadStateScheduler(AgentScheduler):
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

        self.filename = common.project.replace(
            "src", 'tmp/sp_st_log_temp.%s.txt' % os.getpid())

        #self.connectionLog = np.empty((0, 5))

        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.ff = open(self.filename, 'w')
        self.writer = csv.writer(self.ff)
        self.chunk = []
        self.active = common.writeActivations  # TODO add writeSpreadStates to config.ini file
        printHeader(
            self.writer,
            firstline=['#spreadStatelog'],
            lastline=['time', 'agent', 'state1', 'state2'])
        common.sprlog = self

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
        self.register_entry_in_chunk([date, agent, state1, state2])
