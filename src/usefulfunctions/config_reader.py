import commonVar as common

from configparser import ConfigParser


class ConfigReader():
    """

    ConfigReader
    Class of all the Schedulers for the agents

    """

    def __init__(self):
        self.configFile = ""
        self.config = ConfigParser()

    def setCommonVars(self):
        # INIT
        #common.SEED = self.config['INIT'].getint('SEED')
        common.N_USERS = self.config['INIT'].getint('N_USERS')
        common.N_SOURCES = self.config['INIT'].getint('N_SOURCES')
        common.N_CYCLES = self.config['INIT'].getint('N_CYCLES')
        common.N_AGENTS = common.N_USERS + common.N_SOURCES
        common.averageDegree = self.config['INIT'].getfloat(
            'averageDegree')
        common.prop = self.config['INIT'].getfloat('prop')
        common.P_a = common.averageDegree / common.N_USERS
        common.P_s = common.prop * common.P_a

        # USER
        common.dim = self.config['USER'].getint('dim')
        common.memorySize = self.config['USER'].getint('memorySize')

        # SOURCE
        common.overwrite = self.config['SOURCE'].getboolean('overwrite')

        # EXEC
        common.pInitActivation = self.config['EXEC'].getfloat(
            'pInitActivation')
        common.tRemember = self.config['EXEC'].getfloat('tRemember')
        common.pForget = self.config['EXEC'].getfloat('pForget')
        common.vOld = self.config['EXEC'].getfloat('vOld')
        common.pActivation = self.config['EXEC'].getfloat('pActivation')
        common.tInactivation = self.config['EXEC'].getfloat(
            'tInactivation')
        common.pInactivation = self.config['EXEC'].getfloat(
            'pInactivation')
        common.pChange = self.config['EXEC'].getfloat('pChange')
        common.pActiveDiffusion = self.config['EXEC'].getfloat(
            'pActiveDiffusion')
        common.tActiveDiffusion = self.config['EXEC'].getfloat(
            'tActiveDiffusion')
        common.pWeight = self.config['EXEC'].getfloat('pWeight')
        common.pRemove = self.config['EXEC'].getfloat('pRemove')
        common.tCreateEdge = self.config['EXEC'].getfloat('tCreateEdge')
        common.pDeleteEdge = self.config['EXEC'].getfloat('pDeleteEdge')

        # SLAPP
        common.verbose = self.config['SLAPP'].getboolean('verbose')
        common.projectVersion = self.config['SLAPP'].get(
            'projectVersion')
        common.toBeExecuted = self.config['SLAPP'].get('toBeExecuted')
        common.debug = self.config['SLAPP'].getboolean('debug')

        # FLAGS
        common.toggleForgetNews = self.config['FLAGS'].getboolean(
            'toggleForgetNews')
        common.toggleTiredness = self.config['FLAGS'].getboolean(
            'toggleTiredness')
        common.toggleCutOldest = self.config['FLAGS'].getboolean(
            'toggleCutOldest')
        common.toggleActivateWithProba = self.config['FLAGS'].getboolean(
            'toggleActivateWithProba')

        # LOG
        common.writeConnections = self.config['LOG'].getboolean(
            'writeConnections')
        common.writeMessages = self.config['LOG'].getboolean(
            'writeMessages')
        common.writeMemories = self.config['LOG'].getboolean(
            'writeMemories')
        common.writeActivations = self.config['LOG'].getboolean(
            'writeActivations')
        common.lineBuffer = self.config['LOG'].getint('lineBuffer')

    def readConfigFile(self, configFile):
        self.configFile = configFile
        self.config.read(self.configFile)
        print(self.configFile)