# User.py
import sys
import random

import commonVar as common
#import sky.skyagent.agentscheduler.MessageScheduler as ms
import numpy as np
import datastructures.database as db
import datastructures.news as nw

from random import choice
from string import digits, ascii_lowercase, ascii_uppercase

from agTools import *
#from numpy import linalg as LA
from Tools import *
from world.WorldAgent import *
from usefulfunctions.useful_functions import norm
from usefulfunctions.cumulative_functions import power_cumulative


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

    def __init__(self, number, myWorldState, agType):
        super().__init__(number, myWorldState, agType)

        self.database = db.database()  # News database
        self.dblacklist = db.database()  # Blacklist database
        self.debunker = False  # Agent is a debunker or not
        self.spreadState = 's'  # Agent starts ignorants
        self.active = True  # Agent is active or not default active
        self.inactiveTime = 0  #
        self.activeTime = 0  #
        self.activate_agent()  # Agent starts active or inactive randomly
        self.genState(n=0, noise=0.15)  # mind state is generated
        self.tiredness = 1  # agent starts not tired
        self.prevDiff = 'a' if random.random(
        ) < 0.5 else 'p'  # random rpevious diffusion to prevent otherDiffusion from failing

    #def __repr__(self):
    #    print("User()")

    def __str__(self):
        try:
            return (
                '===================\n' + 'User\n' + '-------------------\n' +
                'number: {0}\nspread state: {1}\nactive: {2}\n' +
                '===================').format(self.number, self.spreadState,
                                              self.active)
        except TypeError as ter:
            return "Type Error"

    def activate_debunker(self, p=common.pInitDebunker):
        """Initial debunking initialization

        TODO NO DEBUNKERS RIGHT NOW
        """
        if p == 1:
            self.debunker = True
        elif random.random() > p:
            self.debunker = False
        else:
            self.debunker = True

    def activate_agent(self, p=common.pInitActivation):
        """Initial activity initialization

        activate the agent with a probability p.
        Used at initialization

        """
        if common.toggleActivation is False:
            return
        if p == 1:
            self.active = True
            self.inactiveTime = random.randint(0, 5)
        elif random.random() > p:
            self.active = False
            self.inactiveTime = random.randint(0, 5)
        else:
            self.active = True
            self.activeTime = random.randint(0, 1)

    #def norm(self, x, ord=None, axis=None, keepdims=False):
    #    """
    #    return norm of vector.
    #    different norms can be chosen
    #
    #    """
    #    return norm(x)
    #    # return x / LA.norm(x, ord=ord, axis=axis, keepdims=keepdims)

    def get_list_of_all_self_neighbors(self):
        """return neighbour list. call with no arguments
        """
        return list(common.G.neighbors(self.number))

    def get_list_of_all_active_neighbors(self):  # NOT TESTED YET
        """return a list of only active neighbors
        """
        n = list(common.G.neighbors(self.number))
        return [x for x in n if common.G.node[x].active is True]

    def is_user(self, n):
        """return True if node n is a user
        """
        if common.G.node[n]['agent'].agType == 'users':
            return True
        return False

    def is_memory_empty(self):
        """return True if memory empty
        """
        return True if len(self.database) == 0 else False

    def getStateFromNode(self, n):
        """

        return state from agent in node n

        """

        return common.G.nodes(data=True)[n][1]['agent'].state

    def add_edge(self, n, weight=0.3 + 0.7 * random.random()):
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
            write=common.writeConnections)

    def remove_edge(self, n):
        """

        removes link with a node with id a

        """

        common.conlog.registerEntry(
            first=self.number,
            second=n,
            date=common.cycle,
            weight=common.G[self.number][n]['weight'],
            cr='r',
            write=common.writeConnections)
        common.G.remove_edge(self.number, n)

    def updateWeight(self, neighbor, value, r=common.pRemove):
        """ Takes two nodes, the weight to update
        and comunicates the changes to the conlog
        """
        common.G[self.number][neighbor]['weight'] += value
        common.conlog.registerEntry(
            first=self.number,
            second=neighbor,
            date=common.cycle,
            weight=common.G[self.number][neighbor]['weight'],
            cr='u',
            write=common.writeConnections)
        if common.G[self.number][neighbor]['weight'] < r:
            ##
            ## TWO CALLS TO CONLOG
            ##
            common.conlog.registerEntry(
                first=self.number,
                second=neighbor,
                date=common.cycle,
                weight=common.G[self.number][neighbor]['weight'],
                cr='r',
                write=common.writeConnections)
            self.remove_edge(neighbor)

    def distance(self, n, a='scalar'):
        """

        Return state distance between self state and another vector.

        if you want to use different distances use the parameter a.

        n: np.array of memory size

        scalar: use scalar product


        """

        if a == 'scalar':
            return np.dot(self.state, n)

    def distance_s1_s2(self, s1, s2):
        return np.dot(s1, s2)

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
                del (self.database[key])
                return True
        return False

    def cut_oldest_news(self):
        """

        forget oldest news

        """
        tdate = sys.maxsize
        kmin = 0
        for key in self.database:
            if self.database[key]['date-creation'] < tdate:
                tdate = self.database[key]['date-creation']
                kmin = key
            del (self.database[kmin])
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
                forgot = self.database[random.choice(list(self.database))]
                if news == 0:
                    del (forgot)
                    return True

                elif forgot != news:
                    #uf.vprint("Agent", self.number, "forgot", forgot)
                    del (forgot)
                    return True
                else:
                    return False

    def remember(self,
                 news,
                 cutoldest=common.toggleCutOldest,
                 forgetNews=common.toggleForgetNews,
                 tiredness=common.toggleTiredness,
                 threshold=common.tRemember,
                 rnd=common.pForget,
                 id_send=-1):
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
                self.cut_oldest_news()
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

    def blacklist(self, news, t=common.blacklistOld, e=common.blacklistError):
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

    def findKeyDistanceMinMax(self, data, innerkey, minor=True, a='scalar'):
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

    def switch_activation(self):
        """ Switch active state of an agent

        switches activation of the user and resets the counters
        """

        if common.toggleActivation is False:
            return
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

    def time_state_activation(self):  ########################################
        """If active return active state
        If inactive inactiveState
        """
        if self.active is True:
            return self.activeTime
        return self.inactiveTime

    def continue_state_activation(self):
        """The agents stays in its active or inactive state

        Increments the correct active or inactive time of the agent

        returns True if agent is active

        returns False if agent is inactive
        """
        if self.active is True:
            self.activeTime += 1
            return True

        self.inactiveTime += 1
        return False

    def change_activation_with_probability(self, x, function, par):
        """Uses a function defined in commonVar to determine
        the  probability of activation
        """
        if random.random() < function(x, par):
            self.continue_state_activation()
            return True
        self.switch_activation()
        return False

    def readNews(self, old=common.vOld):
        """

        read news from node n
        return all the possible readable news in a dictionary of news


        remove the oldest
        old: default 24. hours in which the news gets old

        see 'getAllNewsFromSource' and 'getAllNewsFromUser'

        """

        temp = []
        l = self.get_list_of_all_self_neighbors()
        for ne in l:
            if self.is_user(ne):
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
            data=common.G.node[n]['agent'].database,
            innerkey='new',
            minor=False)
        return (n, tdata)

    def becomeActive(self, t=common.tActivation, p=common.pActivation):
        """

        Used only if ACTIVATION

        If user is inactive for some time t
        become active with a probability p

        t: threshold of inactiveTime. The user will not activate for sure
        under the threshold

        p: probability of activation

        """
        ##############################################
        #
        # DEPRECATING
        #
        #############################################
        print("deprecated function: if you see this message it's no good")
        pass

        if common.toggleActivation is False:
            return
        if common.toggleActivateWithProba is True:
            return
        if self.inactiveTime >= t:
            if random.random() < common.timeActiveArray[self.inactiveTime - 1]:
                # if random.random() < 1 - p *
                # np.exp(-self.inactiveTime):
                self.switch_activation()

    def becomeInactive(self,
                       t=common.tInactivation,
                       p=common.pInactivation,
                       tiredness=common.toggleTiredness,
                       probabilityFunction=0):
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
        ##############################################
        #
        # DEPRECATING
        #
        #############################################
        print("deprecated function: if you see this message it's no good")
        pass

        if probabilityFunction != 0:
            return True
        if tiredness is True:
            p = p * self.tiredness
        if self.activeTime > t:
            if random.random() < common.timeInactiveArray[self.activeTime - 1]:
                self.switch_activation()
                #self.tiredness = 1

    def checkActivation(
            self,
            t_inactive=common.tInactivation,
            t_active=common.tActivation,
            p_active=common.pActivation,
            p_inactive=common.pInactivation,
            tiredness=common.toggleTiredness,
    ):
        """

        Activates a sleeping node
        also checks active state with true or false

        Possibly changeable in the future

        """

        ##############################################
        #
        # DEPRECATING
        #
        #############################################
        print("deprecated function: if you see this message it's no good")
        pass

        if common.toggleActivation is False:
            return True
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

        ##########################################
        #
        # Activation is handled out of the
        # diffusion functions
        #
        #
        ##########################################
        #
        #if common.toggleActivateWithProba is True:
        #    active = self.probaActivation(
        #        x=self.timeStateActivation(),
        #        function=common.cumulative,
        #        par=common.argCumulative)
        #    if active is False:
        #        return False
        #else:
        #    if self.checkActivation() is False:
        #        return False
        #
        #########################################

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
                write=common.writeMessages)
        #
        # register news in memory
        remembered = self.remember(iWantToRemember)
        #
        ##########################################
        #
        # Activation is handled out of the
        # diffusion functions
        #
        #
        ##########################################
        # tries to become inactive
        #self.becomeInactive()
        #
        #########################################
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
        self.state = norm(self.state)
        return True

    def change_spreading_state(self, state):
        """
        Changes the spreading state of a user and calls
        the logger if changed
        returns True if the state changed
        """
        oldstate = self.spreadState
        self.spreadState = state
        if oldstate != state:
            common.sprlog.registerEntry(
                date=common.cycle,
                agent=self.number,
                state1=oldstate,
                state2=state)
            return True
        return False

    def is_conected_with_only_sources(self):
        """

        if user is connected only with sources return True

        """
        if any(
            [self.is_user(x)
             for x in self.get_list_of_all_self_neighbors()]) is False:
            return True
        else:
            return False

    def is_connected_with_only_state(self, state='r'):
        """
        if user is connected with only state return True"""
        if all([
                common.G.node[i]['agent'].spreadState == state
                for i in self.get_list_of_all_self_neighbors()
        ]):
            return True
        return False

    def active_diffusion(self,
                         p=common.pActiveDiffusion,
                         threshold=common.tActiveDiffusion,
                         q=common.pWeight,
                         r=common.pRemove,
                         tiredness=common.toggleTiredness):
        """Active diffusion

        performs active diffusion with the best news in memory
        the spread goes in two directions

        one to the neighbour with highest weight
        the orher randomly to a neighbour
        """
        #
        # SELF CHECKING: CAN I DIFFUSE?
        #
        # cannot diffuse if is S or R
        if self.spreadState == 's' or self.spreadState == 'r':
            return False
        #
        # cannot diffuse if is inactive
        if self.active == False:
            return False
        ##########################################
        #
        # Activation is handled out of the
        # diffusion functions
        #
        #
        ##########################################
        #
        #if self.checkActivation() is False:
        #    return False
        #
        ##########################################
        #
        # check if memory is empty
        if self.is_memory_empty():
            return False
        #
        # check if user is connected only to sources
        # active diffusion is performed with users
        ####################################################### DEPRECATING
        if self.is_conected_with_only_sources() is True:
            print("THIS FUNCTION WILL BE DEPRECATED SOON")
            return False
        ###################################################################
        #
        # Find best news in memory based on distance
        bestNews = self.findKeyDistanceMinMax(
            self.database, 'new', minor=False)

        #
        # Find the best neighbour based on weight
        bestWeight = 0
        bestNeighbour = self.number
        for neighbour in self.get_list_of_all_self_neighbors():
            #
            # NOT SELF CHECKING: CAN I DIFFUSE TO...?
            #
            # do not diffuse to source
            ####################################################### DEPRECATING
            if self.is_user(neighbour) is False:
                continue
            ###################################################################
            #
            # look for bestweight
            if common.G.get_edge_data(*(self.number,
                                        neighbour))['weight'] > bestWeight:
                bestWeight = common.G.get_edge_data(*(self.number,
                                                      neighbour))['weight']
                bestNeighbour = neighbour

        #
        # Find a random neighbor
        listOfNeighbors = self.get_list_of_all_self_neighbors()
        if common.toggleDiffuseToInactive is False:
            # if cannot diffuse to inactive filter active neighbors
            # from all neighbors
            listOfNeighbors = [
                ne for ne in listOfNeighbors
                if common.G.node[ne]['agent'].active == True
            ]
        # if no active neighbors take 0 as shuffledNeighbor
        if listOfNeighbors == []:
            shuffledNeighbor = -1
        # if active neighbors exist take one random
        else:
            while True:
                shuffledNeighbor = random.choice(listOfNeighbors)
                if self.is_user(shuffledNeighbor) is True:
                    break
                print("this is a warning. you are not supposed to read this")

        finalNeighbour = bestNeighbour
        if common.toggleDiffuseToInactive is False:
            # If best neighbor is non active chose random active neigbor
            # If no active neighbor => become stifler
            if common.G.node[finalNeighbour]['agent'].active is False:
                finalNeighbour = shuffledNeighbor

        # chose random neighbor with proba p
        if random.random() < p:
            finalNeighbour = shuffledNeighbor
        else:
            finalNeighbour = bestNeighbour

        # DEPRECATED ##########################################################
        #
        # find random user neighbor
        #while True:
        #    shuffledNeighbor = random.choice(
        #        self.get_list_of_all_self_neighbors())
        #    if self.is_user(shuffledNeighbor) is True:
        #        break
        #######################################################################
        #
        #
        # If final neighbor is infected or all neighbors are inactive
        if finalNeighbour < 0 or common.G.node[finalNeighbour][
                'agent'].spreadState == 'i':
            self.become_stifler()
        elif common.G.node[finalNeighbour]['agent'].spreadState == 'r':
            self.become_stifler()
        #
        # If final neighbor is non infective and non 0
        else:
            ### begin old news block
            #
            # if news is too old
            if common.toggleOldNews is True:
                if common.cycle - bestNews['date-creation'] - common.vOld > 0:
                    if random.random() < (1 - np.exp(
                            -0.5 * (common.cycle - bestNews['date-creation'] -
                                    common.vOld))):
                        common.G.node[finalNeighbour]['agent'].become_stifler()
                        self.become_stifler()
                        return
            ### end old news block

            ### begin immunity block
            #  _                                 _ _
            # (_)_ __ ___  _ __ ___  _   _ _ __ (_) |_ _   _
            # | | '_ ` _ \| '_ ` _ \| | | | '_ \| | __| | | |
            # | | | | | | | | | | | | |_| | | | | | |_| |_| |
            # |_|_| |_| |_|_| |_| |_|\__,_|_| |_|_|\__|\__, |
            #                                          |___/
            #
            #  _     ____       ___    ___       _ _
            # / |   |___ \     ( _ )  ( _ )     | | |
            # | |     __) |    / _ \/\/ _ \/\   | | |
            # | |_   / __/ _  | (_>  < (_>  <_  | | |
            # |_( ) |_____( )  \___/\/\___/\( ) | | |
            #   |/        |/                |/  |_|_|
            #
            tnews = False
            tagent = False
            dagent = self.distance(
                common.G.node[finalNeighbour]['agent'].state)
            dnews = self.distance_s1_s2(
                bestNews['new'], common.G.node[finalNeighbour]['agent'].state)

            if dagent < common.tImmunityA:
                if random.random() < 1 - dagent:
                    tagent = True
            if dnews < common.tImmunityN:
                if random.random() < 1 - dnews:
                    tnews = True
            # 1
            # if too distant from spreader
            if common.toggleThresholdOnAgents is True and common.toggleThresholdOnNews is False:
                if tagent is True:
                    common.G.node[finalNeighbour]['agent'].become_stifler()
                    return
            # 2
            # if too distant from news
            elif common.toggleThresholdOnNews is True and common.toggleThresholdOnAgents is False:
                if tnews is True:
                    common.G.node[finalNeighbour]['agent'].become_stifler()
                    return
            elif common.toggleThresholdOnNews is True or common.toggleThresholdOnAgents is True:
                if tnews is True and tagent is True:
                    common.G.node[finalNeighbour]['agent'].become_stifler()
                    return
            ### end immunity block
            common.G.node[finalNeighbour]['agent'].remember(bestNews)
            common.msglog.registerEntry(
                id_src=bestNews['id-source'],
                date_creation=bestNews['date-creation'],
                sender=self.number,
                reciver=bestNeighbour,
                id_new=bestNews['id-n'],
                date=common.cycle,
                diffusion='a',
                write=common.writeMessages)
            # become infected
            common.G.node[finalNeighbour]['agent'].change_spreading_state('i')

            dist = common.G.node[finalNeighbour]['agent'].distance(
                bestNews['new'])
            #
            # bad news
            if dist < threshold:
                value = -q * dist
                self.updateWeight(neighbor=finalNeighbour, value=value, r=r)
                #
                # good news
            elif dist > 1 - threshold:
                value = q * dist
                self.updateWeight(neighbor=finalNeighbour, value=value, r=r)
            else:
                # they are still... friends... I guess?
                pass

        if tiredness is True:
            self.tiredness = self.tiredness * 1.3

        #self.switch_activation()
        return True

    def preferential_add_edge(self, threshold=common.tCreateEdge):
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
        if self.get_list_of_all_self_neighbors() == []:
            if d1 > threshold:
                self.add_edge(n1)
                return True
            return False
        for firstnode in self.get_list_of_all_self_neighbors():
            #
            # check if user is connected only to sources
            if self.is_conected_with_only_sources() is True:
                return False
            #
            # skip adding connection from source
            if self.is_user(firstnode) is False:
                d2 = -1
                continue
            #
            for secondnode in common.G.node[firstnode][
                    'agent'].get_list_of_all_self_neighbors():
                nlist.append(secondnode)
                dlist.append(
                    self.distance(common.G.node[secondnode]['agent'].state))
        nlist = [x for (y, x) in sorted(zip(dlist, nlist))]
        while True and not nlist:
            n2 = nlist[random.randint(0, 10)]
            if n2 in self.get_list_of_all_self_neighbors():
                nlist.remove(n2)
                continue
            else:
                break
        d2 = self.distance(common.G.node[n2]['agent'].state)
        if d1 > d2:
            self.add_edge(n1, weight=0.3 + 0.7 * random.random())
        else:
            self.add_edge(n2, weight=0.3 + 0.7 * random.random())
        return True

    def preferential_remove_edge(self, p=0.1):
        """Preferential delete

        deletes a random edge with a low probability or the one
        connected to the agent with lesser distance

        """
        #
        # if empty neighbors
        if self.get_list_of_all_self_neighbors() == []:
            return False
        #
        # if only one neighbor
        if len(self.get_list_of_all_self_neighbors()) == 1:
            return False
        #
        # remove edge randomly
        if random.random() < p:
            self.remove_edge(
                random.choice(self.get_list_of_all_self_neighbors()))
            return True
        #
        # or
        #
        # remove the most distant neighbor
        d = 1
        n = self.number
        for node in self.get_list_of_all_self_neighbors():
            if self.distance(common.G.node[node]['agent'].state) < d:
                d = self.distance(common.G.node[node]['agent'].state)
                n = node
        self.remove_edge(n)
        return True

    def has_news_in_database(self, id_source=0, date=1):
        """

        chech if user has a certain news inside his memory
        overloaded from WorldAgent

        """

        if self.database == {}:
            return False
        for key in self.database:
            if self.database[key]['id-source'] == id_source and self.database[
                    key]['date-creation'] == date:
                return True
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

    def random_diffusion(self):
        """
        one diffusion at random
        """
        if random.random() < 0.5:
            self.passiveDiffusion()
            self.prevDiff = 'p'
        else:
            self.active_diffusion(
                p=common.pActiveDiffusion,
                threshold=common.tActiveDiffusion,
                q=common.pWeight,
                r=common.pRemove)
            self.prevDiff = 'a'

    def other_diffusion(self):
        """
        if activediffusion -> passivediffuson
        else -> activediffusion
        """
        if self.prevDiff == 'p':
            self.active_diffusion(
                p=common.pActiveDiffusion,
                threshold=common.tActiveDiffusion,
                q=common.pWeight,
                r=common.pRemove)
        else:
            self.passiveDiffusion()

    #######################################################
    # imported from source

    def create_news(self, p=0.1):
        """

        creates one news 'near' to the source's mind state
        this can be used only by Sources -> Infected -> i
        """
        if self.spreadState != 'i':
            return None
        tmp = self.state
        for j in range(common.dim):
            tmp[j] += 0.1 * random.random()
        tmp = norm(tmp)
        return tmp

    def generate_news(self, n=1):
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

        # can be used only by sources -> infected -> i
        if self.spreadState != 'i':
            return

        # the first part is the id-source, id-mittant, time
        self.database = db.database()
        for i in range(n):
            #stringa = binascii.b2a_hex(os.urandom(8))
            allchars = digits + ascii_lowercase + ascii_uppercase
            stringa = "".join([choice(allchars) for i in range(16)])
            self.database[stringa] = {}
            self.database[stringa]['id-n'] = stringa
            self.database[stringa]['new'] = self.create_news()
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

    # end importing from source
    #########################################################

    def become_stifler(self, probability=common.pStifler):
        """
        user can become stifler only if infected and only if active
        """
        #probability = 1 - (len(self.get_list_of_all_self_neighbors()) / 71)
        if np.random.random() < probability:
            if self.spreadState == 'i' and self.active is True:
                self.change_spreading_state('r')

    def become_active(self):
        if self.active == False:
            self.switch_activation()
            return True
        return False

    def become_inactive(self):
        if self.active == True:
            self.switch_activation()
            return True
        return False

    def random_activation(self):
        if common.toggleActivation is False:
            return
        #rndm = 1. * (len(self.get_list_of_all_self_neighbors()) / 71
        #             )  # 576, 71
        rndm = 0.5
        if random.random() < rndm:
            if self.active == True:
                self.continue_state_activation()
            else:
                self.switch_activation()
        #else:
        #    if self.active == True:
        #        self.switch_activation()
        #    else:
        #        self.continue_state_activation()
        #if self.number == common.source_index:
        #    self.active = True
        #self.change_activation_with_probability(
        #    x=self.time_state_activation(), function=power_cumulative, par=3.5)
        #if np.random.random() < 0.5:
        #    self.active = False
        #else:
        #    self.active = True

    def contact_process(self):
        """Single spreading for each time cycle"""
        if self.number != common.source_index:
            self.apathy()
        self.active_diffusion()

    def truncated_process(self):
        """Spread while agent is infective"""
        if self.number != common.source_index:
            self.apathy()
        while True:
            if self.active == False:
                break
            if self.spreadState != 'i':
                break
            if self.is_connected_with_only_state('r') == True:
                #print("True")
                self.become_stifler()
                break
            self.active_diffusion()

    def activate_spreader(self):
        if common.toggleActivation == False:
            return
        if self.number == common.source_index:
            self.become_active()
            print(self.number)

    def apathy(self, probability=0.005):
        """S->R with proba lambda*(1-p)"""
        if common.toggleApathy == False:
            return
        if self.spreadState != 'i':
            return
        if random.random() > probability:
            self.become_stifler()
