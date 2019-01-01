# AgentScheduler
import os
import shutil

from Tools import *
from agTools import *
from sky.SkyAgent import *

from coloroutput import DEBUG_LABEL, LOG_LABEL, OK_LABEL, INPUT_LABEL, WARNING_MSG, ERROR_MSG
from usefulfunctions.useful_functions import vprint


class AgentScheduler(SkyAgent):
    """

    AgentScheduler
    Class of all the Schedulers for the agents

    """

    def __init__(self, number, myWorldState, agType):
        super().__init__(number, myWorldState, agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType

    def write_and_close_log_file(self, path='./defLog.csv', write=True):
        """
        default write log function
        """
        self.ff.close()
        if write == False:
            vprint(WARNING_MSG + "[", self.agType, ":", self.number,
                   "] write_log() called but not enabled: no file written")
        else:
            try:
                shutil.copy(self.filename, path)
            except EnvironmentError:
                vprint(
                    ERROR_MSG + "[", self.agType, ":", self.number,
                    " ] error copying log file from temporary file. " +
                    "Temporary copy may be here:", self.filename)
            else:
                vprint(OK_LABEL + "[", self.agType, ":", self.number,
                       "] file written at", path)

        try:
            os.remove(self.filename)
        except OSError:
            vprint(ERROR_MSG + "[", self.agType, ":", self.number,
                   "] Error deleting temporary file:", self.filename)
        else:
            vprint(OK_LABEL + "[", self.agType, ":", self.number,
                   "] temporary file removed:", self.filename)
