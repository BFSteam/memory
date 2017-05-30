# SkyAgent
from Tools import *
from agTools import *
from Agent import *


class SkyAgent(Agent):
    """

    SkyAgent
    Class of agents that don't live on the Earth
    but watch the life from above the clouds

                   __
                 .'  `'.
                /  _    |
                #_/.\==/.\   Yeah!
               (, \_/ \\_/  /
                |    -' |
                \   '=  /
                /`-.__.'
             .-'`-.___|__
            /    \       `.


    """

    def __init__(self, number, myWorldState, agType=""):
        Agent.__init__(self, number, myWorldState, agType=agType)
        # the environment
        self.agOperatingSets = []
        self.number = number
        # self.news = np.zeros(common.dim+3) # contiene l'ultima notizia
        # [id-fonte, id-mittente, data, topics(dim)]

        if myWorldState != 0:
            self.myWorldState = myWorldState
        self.agType = agType
