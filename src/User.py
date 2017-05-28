# User.py
from Tools import *
from agTools import *
from Agent import *
import commonVar as common
import numpy as np
import sys
import random
import usefulFunctions as uf


class User(Agent):

    def __init__(self, number, myWorldState, agType=""):
        Agent.__init__(self, number, myWorldState,
                       agType=agType)  # parent constructor
        self.database = {}
        self.active = False
        self.activate()
        self.inactiveTime = 0
        self.activeTime = 0

    def activate(self, p=0.5):
        """

        activate the agent with a probability p.

        """

        if np.random.random_sample() < p:
            self.active = False
        else:
            self.active = True

    def listNeighbours(self):
        """

        return neighbour list. call with no arguments

        """

        print("list neighbours", common.G.neighbors(self.number))
        return common.G.neighbors(self.number)

    def listNeighboursNode(self, n):
        """

        return list of neughbours of a node n

        """

        return common.G.neighbors(n)

    def isUser(self, n):
        """

        return True if node n is a user

        """

        if n < common.N_SOURCES:
            print(n, " is ", False)
            return False
        else:
            print(n, " is ", True)
            return True

    def getStateFromNode(self, n):
        """

        return state from agent in node n

        """

        return common.G.nodes(data=True)[n][1]['agent'].state

    def createEdge(self, n):
        """

        create link with a node with id a

        """

        common.G.add_edge(self.number, n)

    def removeEdge(self, n):
        """

        removes link with a node with id a

        """

        common.G.remove_edge(self.number, n)

    def distance(self, n, a='scalar'):
        """

        Return state distance between self state and another vector.

        if you want to use different distances use the parameter a.

        n: np.array of memory size

        scalar: use scalar product


        """

        if a == 'scalar':
            return np.dot(self.state, n)

    def remember(self, news, cutoldest=True, threshold=0.9, rnd=0.1):
        """

        register news in a log file 'memory'.
        the memory dimension is given from an extern file

        memory is ordered from the past to the present
        due to the append function.

        there are many ways to take care of full memory.
        specify in cut.

        oldest: if memory is 'full' cut the oldest

        """

        # read anything
        if news == {}:
            return False

        print(self.distance(news['new']))
        # if a news is beautiful forget the worse
        if len(self.database) == common.memorySize:
            if self.distance(news['new']) > threshold:
                tmin = 1
                for key in self.database:
                    if self.distance(self.database[key]['new']) < tmin:
                        tmin = self.distance(self.database[key]['new'])
                del(self.database[key])
        # add element to memory
        self.database[news['id-n']] = news    # else append new
        print("Agent", self.number, "remembered", self.database)
        # cut memory
        if cutoldest is True:
            # while len memory > size of memory cut first element
            while len(self.database) > common.memorySize:
                tdate = sys.maxsize
                kmin = 0
                for key in self.database:
                    if self.database[key]['date-creation'] < tdate:
                        tdate = self.database[key]['date-creation']
                        kmin = key
                del(self.database[kmin])
        # random forget
        if np.random.random_sample() < rnd:
            if self.database == {}:
                pass
            else:
                forgot = self.database[random.choice(list(self.database))]
                if forgot != news:
                    print("Agent", self.number, "forgot", forgot)
                    del(forgot)
        return True

    def findKeyMinMax(self, data, innerkey, minor=True):
        """

        Given a dict of dict and an innerkey 'findKeyMinMax' returns the
        key of the minimum innerkey

        minor: minimum if True, else, maximum

        """

        if minor is True:
            tdist = sys.maxsize
            kmin = 0
            for key in data:
                if data[key][innerkey] < tdist:
                    tdist = data[key][innerkey]
                    kmin = key
            return data[kmin]
        else:
            tdist = -sys.maxsize
            kmax = 0
            for key in data:
                if data[key][innerkey] > tdist:
                    tdist = data[key][innerkey]
                    kmax = key
            return data[kmax]

    def findKeyDistanceMinMax(self, data, innerkey, minor=True, a='scalar'):
        """

        Given a dict of dict and an innerkey 'findKeyMinMax' returns the
        key of the minimum distance innerkey

        minor: minimum if True, else, maximum

        """

        if minor is True:
            tdist = sys.maxsize
            kmin = 0
            for key in data:
                if self.distance(data[key][innerkey], a=a) < tdist:
                    tdist = self.distance(data[key][innerkey], a=a)
                    kmin = key
            return data[kmin]
        else:
            tdist = -sys.maxsize
            kmax = 0
            for key in data:
                if self.distance(data[key][innerkey], a=a) > tdist:
                    tdist = self.distance(data[key][innerkey], a=a)
                    kmax = key
            return data[kmax]

    def switchActivation(self):
        """

        switches activation of the user and resets the counters

        """

        if self.active is True:
            self.active = False
        else:
            self.active = True
        self.inactiveTime = 0
        self.activeTime = 0

    def readNews(self, old=24):
        """

        read news from node n
        return all the possible readable news in a dictionary of news


        remove the oldest
        old: default 24. hours in which the news gets old

        see 'getAllNewsFromSource' and 'getAllNewsFromUser'

        """

        temp = {}
        l = self.listNeighbours()
        for ne in l:
            if self.isUser(ne):
                temp.update(self.getAllNewsFromUser(ne))
            else:
                temp.update(self.getAllNewsFromSource(ne))

        """
        # remove old news
        for key in temp:
            if common.cycle - temp[key]['date-source'] > old:
                del temp[key]
        if temp == {}:
            temp = {'empty':{}}
        """
        return temp

    def getAllNewsFromSource(self, n):
        """

        return the source's database: all the news

        return type: database of database

        n: int, id of the agent

        """

        for i, j in enumerate(common.G.nodes()):
            if j == n:
                return common.G.nodes(data=True)[i][1]['agent'].database

    def getAllNewsFromUser(self, n):
        """

        return the best news in the user's database

        return type: database of datbase or empty database

        n: int, id of the agents

        """

        for i, j in enumerate(common.G.nodes()):
            if j == n:
                if common.G.nodes(data=True)[i][1]['agent'].database == {}:
                    return {}
                else:
                    dmax = -1
                    kmax = 0
                    for key in common.G.nodes(data=True)[i][1]['agent'].database:
                        if self.distance(common.G.nodes(data=True)[i][1]['agent'].database[key]['new']) > dmax:
                            dmax = self.distance(common.G.nodes(data=True)[
                                                 i][1]['agent'].database[key]['new'])
                            kmax = key
                return {common.G.nodes(data=True)[i][1]['agent'].database[kmax]['id-n']: common.G.nodes(data=True)[i][1]['agent'].database[kmax]}

    def becomeActive(self, t=7, p=0.08):
        """

        If user is inactive for some time t
        become active with a probability p

        t: threshold of inactiveTime. The user will not activate for sure
        under the threshold

        p: probability of activation

        """

        if self.inactiveTime > t:
            if np.random.random_sample() < self.inactiveTime * p:
                self.switchActivation()

    def becomeInactive(self, t=2, p=0.08, tired=False, tiredness=1.5):
        """

        If user is actie for some time t
        become inactive with a probability p

        if user did aome actions he is tired
        tired and tiredness influences the probability of becoming inactive

        t: threshold of activeTime. The user will not deactivate for sure
        under the threshold

        p: probability of deactivation

        tired: True if the user has done some actions

        tiredness: how much he is tired

        """

        if tired is True:
            p = p * tiredness
        if self.activeTime > t:
            if np.random.random_sample() < self.activeTime * p:
                self.switchActivation()

    def checkActivation(self, t_active=2, t_inactive=7, p_active=0.08, p_inactive=0.08, tired=True, tiredness=1.5):
        """

        Activates a sleeping node
        also checks active state with true or false

        Possibly changeable in the future

        """

        if self.active is False:
            uf.vprint("Agent", self.number, "is active")
            self.inactiveTime += 1
            self.becomeActive(t=t_inactive, p=p_inactive)
            return False
        else:
            uf.vprint("Agent", self.number, "is active")
            self.activeTime += 1
            return True

    def passiveDiffusion(self):
        """

        performs a passive diffuzion of news between 
        all the nearest neighbours

        """

        newsToChose = self.readNews()
        iWantToRemember = self.chooseNews(newsToChose)
        self.becomeInactive(tired=self.remember(iWantToRemember))

    def activeDiffusion(self):
        """

        performs active diffusion with the best news in memory
        the spread goes in two directions

        one to the neighbour with highest weight
        the orher randomly to a neighbour

        """

        if len(self.database) == 0:
            return False
        bestNews = self.findKeyDistanceMinMax(
            self.database, 'new', minor=False)
        bestWeight = 0
        bestNeighbour = self.number
        for neighbour in self.listNeighbours():
            if common.G.get_edge_data(*(self.number, neighbour))['weight'] > bestWeight:
                bestWeight = common.G.get_edge_data(
                    *(self.number, neighbour))['weight']
                bestNeighbour = neighbour
        print("#100000")
        common.G.nodes(data=True)[bestNeighbour][1]['agent'].remember(bestNews)
        print("#200000")
        shuffledNeighbour = random.choice(self.listNeighbours())
        print("2.50000")
        common.G.nodes(data=True)[
            shuffledNeighbour][1]['agent'].remember(bestNews)
        print("#30000")
        return True

    def firstAction(self):
        """

        bunch of actions

        """

        if self.checkActivation(t_inactive=3, p_inactive=0.08) is True:
            self.passiveDiffusion()
            self.activeDiffusion()

    def hasNews(self, id_source=0, date=1):
        """

        chech if user has a certain news inside
        overloaded from Agent

        """

        if self.database == {}:
            return False
        for key in self.database:
            if self.database[key]['id-source'] == id_source and self.database[key]['date-creation'] == date:
                return True
            else:
                return False

    def chooseNews(self, newsdict):
        """

        takes dict of dicts as argument
        returns the best internal dict according to the distance

        """

        if newsdict == {}:
            return newsdict
        temp = -1
        for key in newsdict:
            if self.distance(newsdict[key]['new']) > temp:
                temp = self.distance(newsdict[key]['new'])
        return newsdict[key]
