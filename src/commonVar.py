"""
commonVar is used by slapp for default variables
some variables can be overwritten by AgentConfigReader
other variabes cannot be overwritten
it is safer to use config.ini of AgentConfigReader

UNSAFE FOR DUPLICATE VARIABLES! USE AgentConfigReader
"""
import datetime
import usefulfunctions.cumulative_functions as cf
from usefulfunctions.useful_functions import hill
#
configFile = "config.ini"

# ---------------------------------------------------------------------
#
# Initial parameters initialization
#
# from here, variables can be overwritten by AgentConfigReader
# default values below
#
# seed used in simulation
SEED = 1

# number of users
N_USERS = 1

# number of sources
N_SOURCES = 0

# number of total agents
N_AGENTS = N_USERS + N_SOURCES

# number of total iterations
N_CYCLES = 1000

# default average degree
averageDegree = 5

# proportionality between P_s and P_a
prop = 10.

# --------------------------------------------------------------------
#
# User initialization
#
# mind state dimension
dim = 3

# memory dimension
memorySize = 12

blacklistSize = 10

blacklistOld = 1000

blacklistError = 0.1

# ---------------------------------------------------------------------
#
# Sources initialization
#
# sources can overwrite news when creating newer
overwrite = True

# ---------------------------------------------------------------------
#
# during execution
#
# User -> debunker #

# probability of being a debunker
pInitDebunker = 0.

# User -> activate #

# probability of first activation of users
pInitActivation = 0.7

# User -> remember #

# threshold above that a news is beautiful
tRemember = 0.9

# probability to forget a news
pForget = 0.05

# User -> readNews #

# value of an old news
vOld = 24

# User -> becomeActive #

# cutoff of inactivation
tActivation = 3

# probability of 'first' activation
pActivation = 0.08

# User -> becomeInactive #

# cutoff of activation
tInactivation = 2

# probability of 'first' activation
pInactivation = 0.08

# User -> changeState #

# weight of changing state
pChange = 0.5

# User -> activeDiffusion #

# probability to diffuse to a random neighbour
pActiveDiffusion = 0.1

# threshold between what influence the link
tActiveDiffusion = 0.1

# weight of weight change
pWeight = 0.1

# value of weight below which there is rimotion
pRemove = 0.1

# User -> createEdge #

# threshold of random creation if the node is without connections
tCreateEdge = 0.6

# User -> deleteEdge #

# probability of removing a random edge
pDeleteEdge = 0.1

# ---------------------------------------------------------------------
#
# SLAPP initialization
#
# the output is more verbose
verbose = True

# project version used by SLAPP
projectVersion = 0.0

# final instruction
toBeExecuted = "print ('Goodbye')"

# SLAPP variable
debug = True

# ---------------------------------------------------------------------
#
# Program flags
#
# agent/deterministic behavior
flags = {
    'toggleForgetNews': True,
    'toggleTiredness': True,
    'toggleCutOldest': True,
    'toggleActivateWithProba': True
}

# function used for activation of agents
cumulative = cf.exponential_cumulative
argCumulative = 1.  # , second argumet for pareto

# ---------------------------------------------------------------------
#
# Log switches and configuration
# Set logs on/off. also set "buffer" size
#
writeConnections = True
writeMessages = True
writeMemories = True
writeActivations = True
lineBuffer = 1000
# ---------------------------------------------------------------------
#
# Variables calculated
#
# P_a and P_s need to be overwritten if one of their dependency
# are. They need also to be computed correctly by AgentConfigReader
#
P_a = float(averageDegree) / N_USERS  # do not overwrite
P_s = prop * P_a  # do not overwrite
# ---------------------------------------------------------------------
#
# These variables have no need to be overwritten
#
# time of simulation
localtime = datetime.datetime.now().strftime("%Y_%d_%m_%H_%M_%S")

# graph address
G = 0
G_labels = 0
G_edge_labels = 0

# custom hill function to activate and deactivate users
# 200 total numerical values pre-computed to optimize speed
timeActiveArray = [
    hill(x + 1, pActivation, tActivation, 3) for x in range(100)
]
timeInactiveArray = [
    hill(x + 1, pInactivation, tInactivation, 3) for x in range(100)
]
# ---------------------------------------------------------------------
