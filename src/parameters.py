# parameters.py
import csv
import random

import commonVar as common
import numpy as np
import usefulfunctions.useful_functions as uf
from usefulfunctions.config_reader import *

from Tools import *


def loadParameters(self):

    # Projct version: contained in commonVariables.py
    try:
        projectVersion = str(common.projectVersion)
    except BaseException:
        projectVersion = "Unknown"
    print("\nProject version " + projectVersion)

    mySeed = int(
        uf.digit_input(
            msg="random number seed (1 to get it from the clock) ", DEFAULT=1))
    common.SEED = mySeed
    if mySeed == 1:
        random.seed()
        np.random.seed()
    else:
        random.seed(mySeed)
        np.random.seed(mySeed)

    common.configFile = input("config file ")
    common.configFile = '../../memory/src/confg.ini' if common.configFile == "" else common.configFile
    """

    nAgents, worldXSize, worldYSize are variables from the object ModelSwarm in ModelSwarm.py


    """
    self.nAgents = 0

    # self.worldXSize= input("X size of the world? ")
    self.worldXSize = 50
    #print("X size of the world? ", self.worldXSize)

    # self.worldYSize= input("Y size of the world? ")
    self.worldYSize = 50
    #print("Y size of the world? ", self.worldYSize)
    """
    common.averageDegree = uf.digit_input(
        msg="Enter average degree for users? (default = " + str(common.averageDegree) + ") ", DEFAULT=common.averageDegree)
    common.P_a = common.averageDegree / common.N_USERS
    common.P_s = 10 * common.P_a
    common.N_AGENTS = common.N_USERS + common.N_SOURCES
    common.N_CYCLES = uf.digit_input(
        msg="How many cycles? (default " + str(common.N_CYCLES) + ") ", DEFAULT=common.N_CYCLES)
    """

    common.configreader = ConfigReader()
    common.configreader.readConfigFile(common.configFile)
    common.configreader.setCommonVars()
    self.nCycles = common.N_CYCLES

    print("using config file ", common.configFile)
    print("using network file ", common.networkfilepath)
    #set variables accordingly to adjacency matrix if defined
    # find maximum number in adjacency matrix
    if common.networkfilepath != "":
        maxnumber = 0
        with open(common.networkfilepath, 'r') as configfile:
            reader = csv.reader(configfile, delimiter=",")
            for row in reader:
                #if row == [] or "" in row: continue
                maxnumber = max(maxnumber, int(row[0]), int(row[1]))

    #count starts from 0
    maxnumber += 1
    print("max number of users found ", maxnumber)
    common.N_USERS = maxnumber - common.N_SOURCES
    common.N_AGENTS = common.N_USERS + common.N_SOURCES
    print("running with ", common.N_USERS, " users and ", common.N_SOURCES,
          " sources")

    # write files users.txt sources.txt accordingly
    #common.N_SOURCES = int(uf.digit_input(
    #    msg="How many sources? (default = " + str(common.N_SOURCES) + ") ", DEFAULT=common.N_SOURCES))
    file = open(common.project + "/sources.txt", "w")
    for i in range(common.N_SOURCES):
        file.write(str(i) + '\n')
    file.close()

    #common.N_USERS = int(uf.digit_input(
    #    DEFAULT=common.N_USERS, msg="How many users? (default = " + str(common.N_USERS) + ") "))
    file = open(common.project + "/users.txt", "w")
    for i in range(common.N_USERS):
        file.write(str(common.N_SOURCES + i) + '\n')
    file.close()
