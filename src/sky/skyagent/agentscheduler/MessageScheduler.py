# AgentScheduler Message Scheduler
import os
import csv
import shutil

import commonVar as common
import numpy as np

from sky.skyagent.AgentScheduler import *
from agTools import *
from Tools import *
from usefulfunctions.useful_functions import printHeader, vprint


class MessageScheduler(AgentScheduler):
    """

    AMMS

    """

    def __init__(self, number, myWorldState, agType=""):
        super(MessageScheduler, self).__init__(
            self, number, myWorldState, agType=agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType

        #self.msgLog = np.empty((0, 7))
        common.msglog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.filename = common.project.replace(
            "src", 'tmp/msg_log_temp.%s.txt' % os.getpid())
        self.ff = open(self.filename, 'w')
        self.w = csv.writer(self.ff)
        printHeader(
            self.w,
            firstline=['#messagelog'],
            lastline=["source", "timec", "news", "ag1", "ag2", "time", "type"])

    def registerEntry(self,
                      id_src=-1,
                      date_creation=-1,
                      sender=-1,
                      reciver=-1,
                      id_new='null',
                      date=-1,
                      diffusion='n',
                      write=True):
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

        self.w.writerow(
            [id_src, date_creation, id_new, sender, reciver, date, diffusion])

    def writeLog(self, path='./defMLog.csv', write=True):
        self.ff.close()
        if write == False:
            vprint(
                "MessageScheduler -> writeLog called but not enabled: no file written"
            )
            os.remove(self.filename)
            return

        shutil.copy(self.filename, path)
        vprint("MessageScheduler -> writeLog file written at", path)
        os.remove(self.filename)
        vprint("MessageScheduler -> writeLog tmp file", self.filename,
               "removed")
