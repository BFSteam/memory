# User.py
import sys
import random

import commonVar as common
#import sky.skyagent.agentscheduler.MessageScheduler as ms
import numpy as np

from agTools import *
#from numpy import linalg as LA
from Tools import *
from world.WorldAgent import *


class User(WorldAgent):
    """
                                                                     ,888888b.
                                                                  .d888888888b
                                                              _..-'.`*'_,88888b
                                                            ,'..-..`"ad88888888b.
                                                                  ``-. `*Y888888b.
                                                                      \   `Y888888b.
    Our Os who art in CPU, LINUX be thy name.                         :     Y8888888b.
    They program run, thy syscalls done, In Kernel as it is in user.  :      Y88888888b.
    Give us this day, our daily code.                                 |    _,8ad88888888.
    And forgive our errors, as we forgive our compilers.              : .d88888888888888b.
    And lead us not into windows, but deliver us from Bill.           \d888888888888888888
    For thine is the serverdom, power, and kernel, for ever. Amen     8888;'''`88888888888
                                                                      888'     Y8888888888
                                                                      `Y8      :8888888888
                                                                       |`      '8888888888
    May GitHub never crash                                             |        8888888888
    Make this code run flawessly                                       |        8888888888
                                                                       |        8888888888
                                                                       |       ,888888888P
                                                                       :       ;888888888'
                                                                        \      d88888888'
                                                                        _.>,    888888P'
                                                                      <,--''`.._>8888(
                                                                       `>__...--' `''`

    """

    def __init__(self, number, myWorldState, agType=""):
        WorldAgent.__init__(self, number, myWorldState,
                            agType=agType)  # parent constructor
        self.database = {}
        self.dblacklist = {}
        self.debunker = False
        self.spreadState = 'i'
        self.active = False
        self.inactiveTime = 0
        self.activeTime = 0
        self.activate()
        self.genState(n=0, noise=0.15)
        self.tiredness = 1
        self.prevDiff = 'a' if random.random() < 0.5 else 'p'

    def activate_debunker(self, p=common.pInitDebunker):
        """Initial debunking initialization
        """
        if p == 1:
            self.debunker = True
        elif random.random() > p:
            self.debunker = False
        else:
            self.debunker = True

    def activate(self, p=common.pInitActivation):
        """Initial activity initialization

        activate the agent with a probability p.
        Used at initialization

        """
        if p == 1:
            self.active = True
            self.inactiveTime = random.randint(0, 5)
        elif random.random() > p:
            self.active = False
            self.inactiveTime = random.randint(0, 5)
        else:
            self.active = True
            self.activeTime = random.randint(0, 1)

    def norm(self, x, ord=None, axis=None, keepdims=False):
        """
        return norm of vector.
        different norms can be chosen

        """
        return x / np.sum(x)
        # return x / LA.norm(x, ord=ord, axis=axis, keepdims=keepdims)

    def listNeighbours(self):
        """return neighbour list. call with no arguments
        """
        return list(common.G.neighbors(self.number))

    def listActiveNeighbors(self):  # NOT TESTED YET
        """return a list of only active neighbors
        """
        n = list(common.G.neighbors(self.number))
        return [x for x in n if common.G.node[x].active == True]

    def isUser(self, n):
        """return True if node n is a user
        """

        if n < common.N_SOURCES:
            return False
        else:
            return True

    def isMemoryEmpty(self):
        """return True if memory empty
        """
        return True if len(self.database) == 0 else False

    def getStateFromNode(self, n):
        """

        return state from agent in node n

        """

        return common.G.nodes(data=True)[n][1]['agent'].state

    def addEdge(self, n, weight=0.3 + 0.7 * random.random()):
        """

        create link with a node with id a

        """

        common.G.add_edge(self.number, n, weight=weight)
        common.conlog.registerEntry(
            first=self.number,
            second=n,
            date=common.cycle,
            weight=weight,
            cr='a',
            write=common.writeConnections
        )

    def removeEdge(self, n):
        """

        removes link with a node with id a

        """

        common.conlog.registerEntry(
            first=self.number,
            second=n,
            date=common.cycle,
            weight=common.G[self.number][n]['weight'],
            cr='r',
            write=common.writeConnections
        )
        common.G.remove_edge(self.number, n)

    def updateWeight(self, neighbor, value, r=common.pRemove):
        """ Takes two nodes, the weight to update
        and comunicates the changes to the conlog
        """
        common.G[self.number][neighbor]['weight'] += value
        if common.G[self.number][neighbor]['weight'] < r:
            self.removeEdge(neighbor)

        common.conlog.registerEntry(
            first=self.number,
            second=neighbor,
            date=common.cycle,
            weight=common.G[self.number][neighbor]['weight'],
            cr='u',
            write=common.writeConnections
        )

    def distance(self, n, a='scalar'):
        """

        Return state distance between self state and another vector.

        if you want to use different distances use the parameter a.

        n: np.array of memory size

        scalar: use scalar product


        """

        if a == 'scalar':
            return np.dot(self.state, n)

    def ifBeautifulForgetWorse(self, threshold=common.tRemember):
        """

        forget worse news if one is very near to threshold

        """
        if len(self.database) == common.memorySize:
            if self.distance(news['new']) > threshold:
                tmin = 1
                for key in self.database:
                    if self.distance(self.database[key]['new']) < tmin:
                        tmin = self.distance(self.database[key]['new'])
                del(self.database[key])
                return True
        return False

    def cutOldestNews(self):
        """

        forget oldest news

        """
        tdate = sys.maxsize
        kmin = 0
        for key in self.database:
            if self.database[key]['date-creation'] < tdate:
                tdate = self.database[key]['date-creation']
                kmin = key
            del(self.database[kmin])
        return True

    def forgetRandomNews(self, news=0, rnd=common.pForget):
        """

        forget random news different from 'news' with probability rnd
        if no argument is provided, forget randomly

        """
        # random forget
        if random.random() < rnd:
            if self.database == {}:
                return False
            else:
                forgot = self.database[random.choice(
                    list(self.database))]
                if news == 0:
                    del(forgot)
                    return True

                elif forgot != news:
                    #uf.vprint("Agent", self.number, "forgot", forgot)
                    del(forgot)
                    return True
                else:
                    return False

    def remember(
            self,
            news,
            cutoldest=common.flags['toggleCutOldest'],
            forgetNews=common.flags['toggleForgetNews'],
            tiredness=common.flags['toggleTiredness'],
            threshold=common.tRemember,
            rnd=common.pForget,
            id_send=-1
    ):
        """

        register news in a log file 'memory'.
        the memory dimension is given from an extern file

        memory is ordered from the past to the present
        due to the append function.

        there are many ways to take care of full memory.
        specify in cut.

        oldest: if memory is 'full' cut the oldest

        """
        #
        # read anything
        if news == {}:
            return False
        #
        # do not remember if it's already present
        #
        # TODO implement here stifler mode???
        #
        if news['id-n'] in self.database:
            return False
        #
        # if a news is beautiful forget the worse
        self.ifBeautifulForgetWorse(threshold=threshold)
        # add element to memory
        # else append new
        ii = news['id-n']
        self.database[ii] = {}
        self.database[ii]['id-n'] = news['id-n']
        self.database[ii]['new'] = news['new']
        self.database[ii]['id-source'] = news['id-source']
        self.database[ii]['date-creation'] = news['date-creation']
        self.database[ii]['relevance'] = news['relevance']
        #
        # while len memory > size of memory cut an element
        # chose between oldest or random news
        while len(self.database) > common.memorySize:
            if cutoldest is True:
                self.cutOldestNews()
            else:
                self.forgetRandomNews(news=0, rnd=1.)
        #
        # forget random news but not the one just remembered
        if forgetNews is True:
            self.forgetRandomNews(news=news, rnd=rnd)
        #
        # tiredness switch
        if tiredness is True:
            self.tiredness = self.tiredness * 1.2
        #
        # if everything went fine return True
        return True

    def isBlacklisted(self, news):
        """Boolean function
        True if news is blacklisted
        """
        if news['id-n'] in self.dblacklist:
            return True
        return False

    def blacklist(
            self,
            news,
            t=common.blacklistOld,
            e=common.blacklistError
    ):
        """Blacklist news

        Blacklist is ordered from past to present

        If blacklistOld == -1 noesn't matter if news is old

        """
        # news already blacklisted
        if self.isBlacklisted(news) in self.dblacklist:
            return False
        ii = news['id-n']
        self.dblacklist[ii] = {}
        self.dblacklist[ii]['id-n'] = news['id-n']
        self.dblacklist[ii]['new'] = news['new']
        self.dblacklist[ii]['id-source'] = news['id-source']
        self.dblacklist[ii]['date-creation'] = news['date-creation']
        self.dblacklist[ii]['relevance'] = news['relevance']

    def findKeyMinMax(self, data, innerkey, minor=True):
        """

        Given a dict of dict and an innerkey 'findKeyMinMax' returns
        the key of the minimum innerkey

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

    def findKeyDistanceMinMax(
            self, data, innerkey, minor=True, a='scalar'):
        """

        Given a dict of dict and an innerkey 'findKeyMinMax' returns the
        database with the innerkey at the min distance

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
        """ Switch active state of an agent

        switches activation of the user and resets the counters
        """

        if self.active is True:
            self.active = False
            self.tiredness = 1
            common.actlog.registerEntry(
                agent=self.number,
                date=common.cycle,
                atype='u',
                atime=self.activeTime)
        else:
            self.active = True
            common.actlog.registerEntry(
                agent=self.number,
                date=common.cycle,
                atype='d',
                atime=self.inactiveTime)
        self.inactiveTime = 0
        self.activeTime = 0

    def timeStateActivation(self):
        """If active return active state
        If inactive inactiveState
        """
        if self.activate is True:
            return self.activeTime
        return self.inactiveTime

    def continueActivation(self):
        """The agents stays in its active or inactive state

        Increments the correct active or inactive time of the agent
        """
        if self.active is True:
            self.activeTime += 1
        else:
            self.inactiveTime += 1

    def probaActivation(self, x, function, par):
        """Uses a function defined in commonVar to determine
        the  probability of activation

        """
        if random.random() < function(x, par):
            self.continueActivation()
            return True
        self.switchActivation()
        return False

    def readNews(self,
                 old=common.vOld):
        """

        read news from node n
        return all the possible readable news in a dictionary of news


        remove the oldest
        old: default 24. hours in which the news gets old

        see 'getAllNewsFromSource' and 'getAllNewsFromUser'

        """

        temp = []
        l = self.listNeighbours()
        for ne in l:
            if self.isUser(ne):
                if self.getAllNewsFromUser(ne) is False:
                    continue
                else:
                    temp.append(self.getAllNewsFromUser(ne))
            else:
                if self.getAllNewsFromSource(ne) is False:
                    continue
                else:
                    temp = temp + self.getAllNewsFromSource(ne)
        return temp

    def getAllNewsFromSource(self, n):
        """

        return the source's database: all the news

        return type: database of database

        n: int, id of the agent

        """
        temp = []
        if common.G.node[n]['agent'].database == {}:
            return False

        for key in common.G.node[n]['agent'].database:
            temp.append((n, common.G.node[n]['agent'].database[key]))

        return temp

    def getAllNewsFromUser(self, n):
        """

        return the best news in the user's database

        return type: database of datbase or empty database

        n: int, id of the agents

        """
        if common.G.node[n]['agent'].database == {}:
            return False
        tdata = self.findKeyDistanceMinMax(
            data=common.G.node[n]['agent'].database, innerkey='new', minor=False)
        return (n, tdata)

    def becomeActive(
            self,
            t=common.tActivation,
            p=common.pActivation,
            probabilityFunction=0
    ):
        """

        If user is inactive for some time t
        become active with a probability p

        t: threshold of inactiveTime. The user will not activate for sure
        under the threshold

        p: probability of activation

        """

        if probabilityFunction == 0:
            pass
        if self.inactiveTime >= t:
            if random.random(
            ) < common.timeActiveArray[self.inactiveTime - 1]:
                # if random.random() < 1 - p *
                # np.exp(-self.inactiveTime):
                self.switchActivation()

    def becomeInactive(
            self,
            t=common.tInactivation,
            p=common.pInactivation,
            tiredness=common.flags['toggleTiredness'],
            probabilityFunction=0
    ):
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
        if probabilityFunction != 0:
            return True
        if tiredness is True:
            p = p * self.tiredness
        if self.activeTime > t:
            if random.random(
            ) < common.timeInactiveArray[self.activeTime - 1]:
                self.switchActivation()
                #self.tiredness = 1

    def checkActivation(
            self,
            t_inactive=common.tInactivation,
            t_active=common.tActivation,
            p_active=common.pActivation,
            p_inactive=common.pInactivation,
            tiredness=common.flags['toggleTiredness'],
    ):
        """

        Activates a sleeping node
        also checks active state with true or false

        Possibly changeable in the future

        """

        if self.active is False:
            #uf.vprint("Agent", self.number, "is active")
            self.inactiveTime += 1
            self.becomeActive(t=t_active, p=p_active)
            return False
        else:
            #uf.vprint("Agent", self.number, "is active")
            self.activeTime += 1
            return True

    def passiveDiffusion(self):
        """

        performs a passive diffusion of news between
        all the nearest neighbours

        newstochoose: list of tuples. the first is a id
        the second is a dictionary
        [ ( 1, {'id-n':dkbjga, ...} ), ... ]

        """
        if common.flags['toggleActivateWithProba'] is True:
            active = self.probaActivation(
                x=self.timeStateActivation(),
                function=common.cumulative,
                par=common.argCumulative)
            if active is False:
                return False
        else:
            if self.checkActivation() is False:
                return False

        #
        # read news
        newsToChose = self.readNews()
        #
        # find best neighbor and news to remember
        bestNeighbour, iWantToRemember = self.chooseNews(newsToChose)
        #
        # register log entry
        if iWantToRemember != {}:
            common.msglog.registerEntry(
                id_src=iWantToRemember['id-source'],
                date_creation=iWantToRemember['date-creation'],
                sender=bestNeighbour,
                reciver=self.number,
                id_new=iWantToRemember['id-n'],
                date=common.cycle,
                diffusion='p',
                write=common.writeMessages
            )
        #
        # register news in memory
        remembered = self.remember(iWantToRemember)
        #
        # tries to become inactive
        self.becomeInactive()
        #
        # update state with news just recived
        self.changeState(iWantToRemember)

    def changeState(self, news, p=common.pChange):
        """ Change state with news content

        Changes state of activation of an agent
        """

        if news == {}:
            return False
        self.state = self.state + p * news['relevance'] * news['new']
        self.state = self.norm(self.state)
        return True

    def onlySources(self):
        """

        if user is connected only with sources return True

        """

        if any([self.isUser(x)
                for x in self.listNeighbours()]) is False:
            return True
        else:
            return False

    def activeDiffusion(
            self,
            p=common.pActiveDiffusion,
            threshold=common.tActiveDiffusion,
            q=common.pWeight,
            r=common.pRemove,
            tiredness=common.flags['toggleTiredness']
    ):
        """Active diffusion

        performs active diffusion with the best news in memory
        the spread goes in two directions

        one to the neighbour with highest weight
        the orher randomly to a neighbour
        """
        #
        # cannot diffuse if is inactive
        if self.checkActivation() is False:
            return False
        #
        # check if memory is empty
        if self.isMemoryEmpty():
            return False
        #
        # check if user is connected only to sources
        # active diffusion is performed with users
        if self.onlySources() is True:
            return False
        #
        #
        bestNews = self.findKeyDistanceMinMax(
            self.database, 'new', minor=False)
        bestWeight = 0
        bestNeighbour = self.number
        for neighbour in self.listNeighbours():
            #
            # d not diffuse to source
            if self.isUser(neighbour) is False:
                continue
            #
            # look for bestweight
            if common.G.get_edge_data(
                    *(self.number, neighbour))['weight'] > bestWeight:
                bestWeight = common.G.get_edge_data(
                    *(self.number, neighbour))['weight']
                bestNeighbour = neighbour

        # find random user neighbor
        while True:
            shuffledNeighbour = random.choice(self.listNeighbours())
            if self.isUser(shuffledNeighbour) is True:
                break
        #
        # chose random neighbor with proba p
        if random.random() < p:
            finalNeighbour = shuffledNeighbour
        else:
            finalNeighbour = bestNeighbour
        #
        #
        common.G.node[finalNeighbour]['agent'].remember(bestNews)
        common.msglog.registerEntry(
            id_src=bestNews['id-source'],
            date_creation=bestNews['date-creation'],
            sender=self.number,
            reciver=bestNeighbour,
            id_new=bestNews['id-n'],
            date=common.cycle,
            diffusion='a',
            write=common.writeMessages
        )

        dist = common.G.node[finalNeighbour]['agent'].distance(
            bestNews['new'])
        #
        # bad news
        if dist < threshold:
            value = -q * dist
            self.updateWeight(neighbor=finalNeighbour,
                              value=value, r=r)
        #
        # good news
        elif dist > 1 - threshold:
            value = q * dist
            self.updateWeight(neighbor=finalNeighbour,
                              value=value, r=r)
        else:
            # they are still... friends... I guess?
            pass

        if tiredness is True:
            self.tiredness = self.tiredness * 1.3

        return True

    def createEdge(self, threshold=common.tCreateEdge):
        """Preferential creation of edge

        adds edge between the user and another node in the graph

        """
        #
        n1 = random.choice(list(common.G.nodes()))
        n2 = random.choice(list(common.G.nodes()))
        nlist = []
        dlist = []
        d1 = -1
        d2 = -1
        #
        # select first with a random choice
        shuf = list(common.G.nodes())
        random.shuffle(shuf)
        for node in shuf:
            # if nodes are not connected pick another one
            if common.G.has_edge(self.number, node) is True:
                continue
            # if picked node is itself pick another one
            if node == self.number:
                continue
            # if picked node is inactive pick another one ############
            # can change in the future
            if common.G.node[node]['agent'].active is False:
                continue
            d1 = self.distance(common.G.node[node]['agent'].state)
            n1 = node
        #
        # check if user is not connected to any node and rewire it
        # randomly
        if self.listNeighbours() == []:
            if d1 > threshold:
                self.addEdge(n1)
                return True
            else:
                return False
        for firstnode in self.listNeighbours():
            #
            # check if user is connected only to sources
            if self.onlySources() is True:
                return False
            #
            # skip adding connection from source
            if self.isUser(firstnode) is False:
                d2 = -1
                continue
            #
            for secondnode in common.G.node[firstnode]['agent'].listNeighbours(
            ):
                nlist.append(secondnode)
                dlist.append(self.distance(
                    common.G.node[secondnode]['agent'].state))
        nlist = [x for (y, x) in sorted(zip(dlist, nlist))]
        while True and not nlist:
            n2 = nlist[random.randint(0, 10)]
            if n2 in self.listNeighbours():
                nlist.remove(n2)
                continue
            else:
                break
        d2 = self.distance(common.G.node[n2]['agent'].state)
        if d1 > d2:
            self.addEdge(n1, weight=0.3 + 0.7 * random.random())
        else:
            self.addEdge(n2, weight=0.3 + 0.7 * random.random())
        return True

    def deleteEdge(self, p=0.1):
        """Preferential delete

        deletes a random edge with a low probability or the one
        connected to the agent with lesser distance

        """
        #
        # if empty neighbors
        if self.listNeighbours() == []:
            return False
        #
        # if only one neighbor
        if len(self.listNeighbours()) == 1:
            return False
        #
        # remove edge randomly
        if random.random() < p:
            self.removeEdge(random.choice(self.listNeighbours()))
            return True
        #
        # or
        #
        # remove the most distant neighbor
        d = 1
        n = self.number
        for node in self.listNeighbours():
            if self.distance(common.G.node[node]['agent'].state) < d:
                d = self.distance(common.G.node[node]['agent'].state)
                n = node
        self.removeEdge(n)
        return True

    def hasNews(self, id_source=0, date=1):
        """

        chech if user has a certain news inside his memory
        overloaded from WorldAgent

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

        temp = -1
        tnum = -1
        tdic = {}
        for number, entry in newsdict:
            if self.distance(entry['new']) > temp:
                temp = self.distance(entry['new'])
                tnum = number
                tdic = entry
        return (tnum, tdic)

    
    def debug(self):
        print(self.number)
        print(self.database)

    def diffusion(self):
        if random.random() < 0.5:
            self.passiveDiffusion()
            self.prevDiff = 'p'
        else:
            self.activeDiffusion(
                p=common.pActiveDiffusion,
                threshold=common.tActiveDiffusion,
                q=common.pWeight,
                r=common.pRemove
            )
            self.prevDiff = 'a'

    def otherDiffusion(self):
        if self.prevDiff == 'p':
            self.activeDiffusion(
                p=common.pActiveDiffusion,
                threshold=common.tActiveDiffusion,
                q=common.pWeight,
                r=common.pRemove
            )
        else:
            self.passiveDiffusion()
