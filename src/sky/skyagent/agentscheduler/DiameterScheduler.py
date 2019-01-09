# Degree Scheduler K Core Scheduler
import csv
import os
import shutil

import commonVar as common
import networkx as nx
import numpy as np
from termcolor import colored
from sky.skyagent.AgentScheduler import *
from agTools import *
from Tools import *

from coloroutput import DEBUG_LABEL, LOG_LABEL, OK_LABEL, INPUT_LABEL, WARNING_MSG, ERROR_MSG
from usefulfunctions.useful_functions import printHeader, vprint


class DiameterScheduler(AgentScheduler):
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
            "src", 'tmp/dmt_log_temp.%s.txt' % os.getpid())

        #self.connectionLog = np.empty((0, 5))

        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.ff = open(self.filename, 'w')
        self.writer = csv.writer(self.ff)
        self.chunk = []
        self.active = common.writeActivations  # TODO add writeSpreadStates to config.ini file
        printHeader(
            self.writer,
            firstline=['# diameterLog'],
            lastline=['time', 'diameter'])
        common.dmtlog = self

    def registerEntry(self, date=-1, graph=None, write=True):
        """

        creates an array to stack under the log and does it

        """
        if write == False:
            return
        diameter = nx.diameter(
            max(nx.connected_component_subgraphs(graph), key=len))
        print("DIAMETER", diameter)
        self.register_entry_in_chunk([date, diameter])
