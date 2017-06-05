# AgentManager Connection Scheduler
from Tools import *
from agTools import *
from AgentManager import *
import numpy as np
import commonVar as common


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

        self.connectionLog = np.zeros([5])

        common.conlog = self

    def printLog(self):
        print(self.connectionLog)

    def registerEntry(
            self,
            first=-1,
            second=-1,
            date=-1,
            weight=-1,
            cr='c',
    ):
        """

        creates an array to stack under the log and does it

        """
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

    def writeLog(self, path='./defCLog.csv'):

        # try to guess extension
        extensions = ('.txt', '.csv')
        ftype = [x for x in extensions if path.endswith(x)][0]
        if ftype == []:
            ftype = '.txt'  # extension not guessed. falling back to txt
        f = open(path, 'w')
        if ftype == '.txt':
            for i in self.connectionLog[1:]:
                if i[4] == 'u':
                    print(
                        "Link",
                        "updated",
                        "between agent",
                        i[0],
                        "and",
                        i[1],
                        "with weight",
                        i[3],
                        "at time",
                        i[2],
                        file=f
                    )
                elif i[4] == 'r':
                    print(
                        "Link",
                        "removed",
                        "between agent",
                        i[0],
                        "and",
                        i[1],
                        "with weight",
                        i[3],
                        "at time",
                        i[2],
                        file=f
                    )

                else:
                    print(
                        "Link",
                        "added",
                        "between agent",
                        i[0],
                        "and",
                        i[1],
                        "with weight",
                        i[3],
                        "at time",
                        i[2],
                        file=f
                    )
        elif ftype == '.csv':
            print("#1", "#2", "#t", "#w", "#@", sep=",", file=f)
            for i in self.connectionLog[1:]:
                print(i[0], i[1], i[2], i[3], i[4], sep=",", file=f)
        else:
            pass
        f.close()
        print("saved", path)
