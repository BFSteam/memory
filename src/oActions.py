import binascii
import csv
import os
import time

import commonVar as common
import graph as graph
import networkx as nx

from termcolor import colored
from Tools import *
from usefulfunctions.useful_functions import worldAgentStringsizer, singleNewsStringsizer, printHeader
from world.WorldAgent import *

import errno
import shutil
from os import listdir
from os.path import isfile, join


def do1b(address):  # visualizeNet in observerActions.txt

    # basic action to visualize the networkX output
    graph.openClearNetworkXdisplay()
    graph.drawGraph()


def do2a(address, cycle):  # ask_all in observerActions.txt
    self = address  # if necessary
    # ask each agent, without parameters
    # if cycle % 25 == 0 :
    #    print("Time =", cycle)

    common.memlog.updateLog(write=common.writeMemories)
    if cycle == 1:
        print("miao")
        common.kcrlog.registerEntry(date=common.cycle, graph=common.G)


def do2b(address, cycle):  # ask_one in observerActions.txt
    """

    Used to save data periodicaly or at a certain time step

    """

    if cycle == address.nCycles:

        # create log directory if it doesn't exist
        if not os.path.exists(common.project.replace("src", "log")):
            os.makedirs(common.project.replace("src", "log"))

        # create destination path and directory appending datetime to logDirName
        destination_path = common.project.replace(
            'src', 'log/' + common.logDirName + '/' + common.localtime + '/')
        try:
            os.makedirs(destination_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        # copy config file
        #shutil.copyfile(
        #    common.configFile,
        #    destination_path + 'config' + str(common.localtime) + '.ini')
        # -------------------------------------------------------------
        if common.writeVariables == True:
            path = destination_path + "variables.csv"
            with open(path, 'w') as variables:
                writer = csv.writer(variables, delimiter=",")
                for i in [
                        item for item in dir(common)
                        if not item.startswith("__")
                ]:
                    writer.writerow([i, getattr(common, i)])
        # -------------------------------------------------------------
        #
        # GML's
        #
        # -------------------------------------------------------------
        #
        # GML
        #
        #path = destination_path + "graph.gml"
        #nx.write_gml(common.G, path, stringizer=worldAgentStringsizer)
        #print("saved", path)
        # -------------------------------------------------------------
        #
        # GML different stringsizer
        #
        # path = common.project.replace(
        #    "src",
        #    "log/graphN" + str(common.localtime) + ".gml")
        # nx.write_gml(common.G, path, stringizer=singleNewsStringsizer)
        # print("saved", path)
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        #
        # AGENT MANAGERS
        #
        # -------------------------------------------------------------
        #
        # CONNECTION LOG
        #
        path = destination_path + "connectionLog.csv"
        common.conlog.write_and_close_log_file(
            path=path, write=common.writeConnections)
        # -------------------------------------------------------------
        #
        # MESSAGE LOG
        #
        path = destination_path + "messageLog.csv"
        common.msglog.write_and_close_log_file(
            path=path, write=common.writeMessages)
        # -------------------------------------------------------------
        #
        # MEMORY LOG
        #
        path = destination_path + "memoryLog.csv"
        common.memlog.write_and_close_log_file(
            path=path, write=common.writeMemories)
        # -------------------------------------------------------------
        #
        # ACTIVATION LOG
        #
        path = destination_path + "activationLog.csv"
        common.actlog.write_and_close_log_file(
            path=path, write=common.writeActivations)
        # -------------------------------------------------------------
        #
        # SPREADING STATE LOG
        #
        path = destination_path + "spreadStateLog.csv"
        common.sprlog.write_and_close_log_file(
            path=path, write=common.writeSpreadStates)
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        #
        # NETWORK MEASURES
        #
        # -------------------------------------------------------------
        #
        # K CORE NEW
        #
        path = destination_path + "k_core.csv"
        # already registered in do2a
        common.kcrlog.registerEntry(date=common.cycle, graph=common.G)
        common.kcrlog.write_and_close_log_file(path=path, write=True)
        # -------------------------------------------------------------
        #
        # DEGREE DISTRIBUTION NEW
        #
        #path = destination_path + "degree_dist.csv"
        #common.deglog.registerEntry(date=common.cycle, graph=common.G)
        #common.deglog.write_and_close_log_file(
        #    path=path, write=common.writeDegree)
        # -------------------------------------------------------------
        #
        # CLUSTERING COEFFICIENT NEW
        #
        #path = destination_path + "clustering.csv"
        #common.clslog.registerEntry(date=common.cycle, graph=common.G)
        #common.clslog.write_and_close_log_file(
        #    path=path, write=common.writeClustering)
        # -------------------------------------------------------------
        #
        # DIAMETER NEW
        #
        #path = destination_path + "diameter.csv"
        #common.dmtlog.registerEntry(date=common.cycle, graph=common.G)
        #common.dmtlog.write_and_close_log_file(
        #    path=path, write=common.writeDiameter)
        # -------------------------------------------------------------

        try:
            from pybeep.pybeep import PyBeep
            PyBeep().beep()
        except BaseException:
            pass


# TODO implement single string replacement
