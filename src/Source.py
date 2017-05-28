# Source.py
from Tools import *
from agTools import *
from Agent import *
import numpy as np
import commonVar as common
import math
import os
import binascii


class Source(Agent):
    """

    Members:

    news: dictionary of dictionaries
    each one contains a news
    the news is made of several voices:
    - id-source: the number of the source
    - id-sender: the number of the last sender
    - date-source: date of creation
    - relevance: importance of the news
    - new: false english to identify a single news
    see generateNews

    reliability: importance of the source

    state: mind state of the source
    each source has almost all components of its state
    of mind near zero
    only one, two or three components are randomly chosen
    to be one
    after the first 'binary' initialization, noise
    is added; the vector is then normalized

    """

    def __init__(self, number, myWorldState, agType=""):
        Agent.__init__(self, number, myWorldState, agType=agType)
        self.news = {}
        self.reliability = np.random.random_sample()

        # source state
        self.state = np.zeros(common.dim)  # inizializzato a zero
        # number of relevant topics for the source: 1, 2 or 3
        r = np.random.randint(1, 4)
        # added r number of ones and noise: the noise is 0.15 for one single
        # topic, 0.1 for 2 and 0.5 for three
        for i in range(r):
            self.state[i] = 1
        for i in range(common.dim):
            self.state[i] += (0.15 / r) * np.random.random_sample()
        # the state is shuffled because the topics are not in a partcular
        # order. then it's normalized
        np.random.shuffle(self.state)
        self.state = self.state / self.state.sum()
        print(self.state)
        if (common.cycle / 100.).is_integer():
            self.generateNews()
        print(self.news)

    def createNews(self, p=0.1):
        """

        creates one news 'near' to the source's mind state

        """

        tmp = self.state
        for j in range(common.dim):
            tmp[j] += 0.1 * np.random.random_sample()
        tmp = tmp / tmp.sum()
        return tmp

    def generateNews(self, n=1):
        """

        generates a dictionary of n news:
        each new is distant from zero to p from
        the mind state of the source

        news{
            n0{
                id-source:...,
                date-source:...,
                new:...,
                ...,
                relevance:...
            }

            n1{...
            }
            ...
        }

        """

        # the first part is the id-source, id-mittant, time
        for i in range(n):
            stringa = binascii.b2a_hex(os.urandom(8))
            self.database[stringa] = {}
            self.database[stringa]['id-n'] = stringa
            self.database[stringa]['new'] = self.createNews()
            self.database[stringa]['id-source'] = self.number
            self.database[stringa]['date-creation'] = common.cycle
            self.database[stringa]['relevance'] = np.random.random_sample()
            self.database[stringa]['id-send'] = self.number
            self.database[stringa]['date-send'] = common.cycle
            self.database[stringa]['id-recive'] = self.number
            self.database[stringa]['date-recive'] = common.cycle

        print(self.number, " generateNews ", n)

    def hasNews(self, id_source=0, date=1):
        if self.database == {}:
            return False
        for key in self.database:
            if self.database[key]['id-source'] == id_source and self.database[key]['date-creation'] == date:
                return True
            else:
                return False
