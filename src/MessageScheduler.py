# AgentManager Message Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common


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

        self.msgLog = np.zeros([7])

        common.msglog = self

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
            diffusion='n'
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

    def writeLog(self, path='./defMLog.csv'):

        # try to guess extension
        extensions = ('.txt', '.csv')
        ftype = [x for x in extensions if path.endswith(x)][0]
        if ftype == []:
            ftype = '.txt'  # extension not guessed. falling back to txt
        f = open(path, 'w')
        if ftype == '.txt':
            for i in self.msgLog[1:]:  # skip the first
                if i[6] == 'a':
                    print("News", str(i[2]),
                          "created by source", str(i[0]),
                          "at cycle", str(i[1]),
                          "diffused passively",
                          "from", str(i[3]),
                          "to", str(i[4]),
                          "at cycle", str(i[5]),
                          file=f
                          )
                elif i[6] == 'p':
                    print("News", str(i[2]),
                          "created by source", str(i[0]),
                          "at cycle", str(i[1]),
                          "diffused passively",
                          "from", str(i[3]),
                          "to", str(i[4]),
                          "at cycle", str(i[5]),
                          file=f
                          )
                else:
                    print("News", str(i[2]),
                          "created by source", str(i[0]),
                          "at cycle", str(i[1]),
                          file=f
                          )
        elif ftype == '.csv':
            print("#s", "#tc", "#n", "#1", "#2", "#t", "#@", sep=",", file=f)
            for i in self.msgLog[1:]:  # skip the first
                print(i[0], i[1], i[2], i[3], i[4],
                      i[5], i[6], sep=",", file=f)
        else:
            pass
        f.close()
        print("saved", path)
