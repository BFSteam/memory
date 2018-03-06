# AgentManager Message Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common
import os, csv
from usefulFunctions import printHeader

class MessageScheduler(AgentManager):
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

        self.msgLog = np.empty((0, 7))
        print(self.msgLog)
        common.msglog = self
        if not os.path.exists(common.project.replace("src", "tmp")):
            os.makedirs(common.project.replace("src", "tmp"))
        self.filename = common.project.replace(
            "src", 'tmp/msg_log_temp.%s.txt' % os.getpid())
        with open(self.filename, 'w') as ff:
            w = csv.writer(ff)    
            printHeader(w, firstline=['#messagelog'],
                        lastline=["source", "timec", "news", "ag1", "ag2", "time", "type"])

    def printLog(self):
        print(self.msgLog)

    def registerEntry(
            self,
            id_src=-1,
            date_creation=-1,
            sender=-1,
            reciver=-1,
            id_new='null',
            date=-1,
            diffusion='n',
            write = True
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
        if write == False: return
        if self.msgLog.shape[0] > 1000:
            with open(self.filename, 'a') as ff:
                w = csv.writer(ff)
                for i in self.msgLog:
                    w.writerow(i[0:7])

            self.msgLog = np.empty((0, 7))
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

    def writeLog(self, path='./defMLog.csv', write=True):

        if write == False:
            print("MessageScheduler->writeLog called but not enabled: no file written")
        # try to guess extension
        with open(self.filename, 'a') as ff:
            w = csv.writer(ff)
            for i in self.msgLog:
                w.writerow(i[0:7])

        with open(path, "w") as fw, open(self.filename, 'r') as fr:
            fw.writelines(l for l in fr)
        os.remove(self.filename)
