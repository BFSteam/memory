# parameters.py
import csv
import random

# color output
from coloroutput import DEBUG_LABEL, LOG_LABEL, OK_LABEL, INPUT_LABEL, WARNING_MSG, ERROR_MSG

import commonVar as common
import networkx as nx
import numpy as np
import usefulfunctions.useful_functions as uf
import sys
from usefulfunctions.config_reader import *

from Tools import *


def loadParameters(self):

    # silly lines for the project version
    # Projct version: contained in commonVariables.py
    try:
        projectVersion = str(common.projectVersion)
    except BaseException:
        projectVersion = "Unknown"
    print("\nProject version " + projectVersion)

    # =========================================================================================
    #
    # GLOBAL SEED IS SET HERE
    #
    print(INPUT_LABEL)
    mySeed = int(
        uf.digit_input(
            msg="random number seed (1 to get it from the clock) ", DEFAULT=1))
    common.SEED = mySeed
    if mySeed == 1:
        # good for now
        # TODO for best practice implement a class like this
        # from https://stackoverflow.com/questions/5012560/how-to-query-seed-used-by-random-random
        #import random
        #
        #class Random(random.Random):
        #    def seed(self, a=None, version=2):
        #        from os import urandom as _urandom
        #        from hashlib import sha512 as _sha512
        #        if a is None:
        #            try:
        #                # Seed with enough bytes to span the 19937 bit
        #                # state space for the Mersenne Twister
        #                a = int.from_bytes(_urandom(2500), 'big')
        #            except NotImplementedError:
        #                import time
        #                a = int(time.time() * 256)  # use fractional seconds
        #
        #        if version == 2:
        #            if isinstance(a, (str, bytes, bytearray)):
        #                if isinstance(a, str):
        #                    a = a.encode()
        #                    a += _sha512(a).digest()
        #                    a = int.from_bytes(a, 'big')
        #
        #        self._current_seed = a
        #        super().seed(a)
        #
        #    def get_seed(self):
        #        return self._current_seed
        random_seed = random.randrange(2**32 - 1)
        random.seed(random_seed)
        np.random.seed(random_seed)
        common.SEED = random_seed
        mySeed = random_seed

    else:
        random.seed(mySeed)
        np.random.seed(mySeed)
    print(WARNING_MSG, "SEED", mySeed)
    #
    # =========================================================================================

    # =========================================================================================
    #
    # SET CONFIG FILE
    #
    print(INPUT_LABEL)
    # set default config file path
    common.configFile = '../../memory/src/confg.ini'
    #ask for config file path
    common.configFile = input("config file [" + common.configFile + "]")
    #set config file path
    common.configFile = '../../memory/src/confg.ini' if common.configFile == "" else common.configFile
    #
    # READ FROM CONFIG FILE AND SET VARIABLES
    #
    common.configreader = ConfigReader()
    common.configreader.readConfigFile(common.configFile)
    common.configreader.setCommonVars()
    print(DEBUG_LABEL + "using config file: ", common.configFile)
    print(DEBUG_LABEL + "using network file: ", common.networkfilepath)
    # this line wal left here to not forget to set the max number of cycles
    self.nCycles = common.N_CYCLES
    print(DEBUG_LABEL + 'number of cycles', common.N_CYCLES)
    #
    # set variables accordingly to adjacency matrix if defined
    # find maximum number in adjacency matrix
    #

    temp_G = nx.Graph()
    temp_degree = []
    temp_kcore = []
    if common.networkfilepath != "":
        maxnumber = 0
        with open(common.networkfilepath, 'r') as configfile:
            reader = csv.reader(configfile, delimiter=",")
            for row in reader:
                #if row == [] or "" in row: continue
                maxnumber = max(maxnumber, int(row[0]), int(row[1]))
                temp_G.add_edge(int(row[0]), int(row[1]))
            temp_kcore = nx.core_number(temp_G)
            temp_degree = nx.degree(temp_G)

    #count starts from 0
    maxnumber += 1
    print(DEBUG_LABEL + "max number of users found ", maxnumber)
    common.N_USERS = maxnumber
    common.N_AGENTS = maxnumber
    print(DEBUG_LABEL + "running with\n", common.N_USERS,
          " (S) SANE/IGNORANT users.\n", common.N_SOURCES,
          " of them are (I) INFECTED/SPREADER")
    print(WARNING_MSG +
          "WARNIG: THIS NEED TO BE CHANGED WITH SPREADERS AND IGNORANTS")
    print(
        WARNING_MSG +
        "THIS WARNING WILL STAY UNTIL CHANGES ON ALL THE PROGRAM ARE COMMITTED"
    )
    print(
        WARNING_MSG +
        'WARNING: Using sources is not possible anymore: define spread state of users instead'
    )
    print(WARNING_MSG + 'testing ... ... ... ...')

    #
    # write files users.txt sources.txt accordingly
    #
    #common.N_SOURCES = int(uf.digit_input(
    #    msg="How many sources? (default = " + str(common.N_SOURCES) + ") ", DEFAULT=common.N_SOURCES))
    #file = open(common.project + "/sources.txt", "w")
    #for i in range(common.N_SOURCES):
    #    file.write(str(i) + '\n')
    #file.close()
    #
    #common.N_USERS = int(uf.digit_input(
    #    DEFAULT=common.N_USERS, msg="How many users? (default = " + str(common.N_USERS) + ") "))
    file = open(common.project + "/users.txt", "w")
    for i in range(common.N_USERS):
        file.write(str(i) + '\n')
    file.close()
    #
    # =========================================================================================

    # =========================================================================================
    #     __    ___ _______  __   __  _______  ____  ______
    #    / /   /   /__  /\ \/ /  /  |/  / __ \/ __ \/ ____/
    #   / /   / /| | / /  \  /  / /|_/ / / / / / / / __/
    #  / /___/ ___ |/ /__ / /  / /  / / /_/ / /_/ / /___
    # /_____/_/  |_/____//_/  /_/  /_/\____/_____/_____/
    #
    # If Lazy Mode is on the input seed is calculated based on the k-core
    # Simulation is performed taking k-core as the initial parameter
    #
    # If Lazy Mode is off input seed is given from input
    #
    print(INPUT_LABEL)
    # raw_input returns the empty string for "enter"
    yes = {'yes', 'y', 'ye'}
    no = {'no', 'n', ''}
    yesnochoice = input('Set "Lazy Mode" on? [y/N]:').lower()
    print(yesnochoice)
    if yesnochoice in yes:
        print("LAZY MODE ON")
        print(INPUT_LABEL)
        s_i = int(
            uf.digit_input(
                msg=
                "initial spreader k-core (insert non positive or none to get it random) ",
                DEFAULT=-1))
        max_si = max(temp_kcore.values())
        ss_ii = [key for key, val in temp_kcore.items() if val == s_i]
        if s_i <= 0 or s_i > max_si or ss_ii == []:
            s_i = np.random.randint(0, common.N_AGENTS)
        else:
            s_i = ss_ii[np.random.choice(len(ss_ii), replace=False)]
        common.source_index = s_i
        #
        # second seed default kcore = 1
        s_i = 1
        ss_ii = [key for key, val in temp_kcore.items() if val == s_i]
        if s_i <= 0 or s_i > max_si or ss_ii == []:
            s_i = np.random.randint(0, common.N_AGENTS)
        else:
            while True:
                s_i = ss_ii[np.random.choice(len(ss_ii), replace=False)]
                if s_i != common.source_index:
                    break
        common.source_index_2 = s_i
        print("SOURCE INDEX", common.source_index)
        print("SOURCE INDEX2", common.source_index_2)
    elif yesnochoice in no:
        print("LAZY MODE OFF")
        print(INPUT_LABEL)
        s_i = int(
            uf.digit_input(
                msg=
                "initial spreader (insert negative or none to get it random) ",
                DEFAULT=-1))
        common.source_index = s_i
        if common.source_index < 0 or common.source_index >= common.N_AGENTS:
            common.source_index = np.random.randint(0, common.N_AGENTS)
        print("SOURCE INDEX", common.source_index)
    else:
        return
        #sys.stdout.write("Please respond with 'yes' or 'no'")
        print("LAZY MODE OFF")
    # =========================================================================================
    #
    # SLAPP OLD VARIABLES UNUSED
    # DO NOT EDIT OR DELETE
    #
    # nAgents, worldXSize, worldYSize are variables from the object ModelSwarm in ModelSwarm.py
    self.nAgents = 0
    # self.worldXSize= input("X size of the world? ")
    self.worldXSize = 50
    #print("X size of the world? ", self.worldXSize)
    # self.worldYSize= input("Y size of the world? ")
    self.worldYSize = 50
    #print("Y size of the world? ", self.worldYSize)
    #
    # =========================================================================================

    # =========================================================================================
    #
    # OLD BLOCK USED WHEN ADJ OR CONFIG FILE IS NOT SPECIFIED
    # DEPRECATING
    #
    #common.averageDegree = uf.digit_input(
    #    msg="Enter average degree for users? (default = " + str(common.averageDegree) + ") ", DEFAULT=common.averageDegree)
    #common.P_a = common.averageDegree / common.N_USERS
    #common.P_s = 10 * common.P_a
    #common.N_AGENTS = common.N_USERS + common.N_SOURCES
    #common.N_CYCLES = uf.digit_input(
    #    msg="How many cycles? (default " + str(common.N_CYCLES) + ") ", DEFAULT=common.N_CYCLES)
    #
    # =========================================================================================
