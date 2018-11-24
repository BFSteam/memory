# Source.py
import binascii
import os
import random

import commonVar as common

from agTools import *
from Tools import *
from world.WorldAgent import *


class Source(WorldAgent):
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
        super(Source, self).__init__(self, number, myWorldState, agType=agType)
        self.news = {}
        self.reliability = random.random()
        self.spreadState = 's'
        self.genState(n=3, noise=0.15)

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
            tmp[j] += 0.1 * random.random()
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
        self.database = {}
        for i in range(n):
            stringa = binascii.b2a_hex(os.urandom(8))
            self.database[stringa] = {}
            self.database[stringa]['id-n'] = stringa
            self.database[stringa]['new'] = self.createNews()
            self.database[stringa]['id-source'] = self.number
            self.database[stringa]['date-creation'] = common.cycle
            self.database[stringa]['relevance'] = random.random()
            common.msglog.registerEntry(
                id_src=self.number,
                date_creation=common.cycle,
                sender=self.number,
                reciver=self.number,
                id_new=stringa,
                date=common.cycle,
                diffusion='c',
                write=common.writeMessages)
        print(self.number, " generateNews ", n)

    def hasNews(self, id_source=0, date=1):
        if self.database == {}:
            return False
        for key in self.database:
            if self.database[key]['id-source'] == id_source and self.database[
                    key]['date-creation'] == date:
                return True
            else:
                return False

    def debug(self):
        print(self.number)
        print(self.database)
