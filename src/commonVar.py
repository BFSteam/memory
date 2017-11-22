# commonVar.py

G = 0  # graph address
G_labels = 0
G_edge_labels = 0

SEED = 1

N_USERS = 200  # number of users

N_SOURCES = 3  # number of sources

N_AGENTS = N_USERS + N_SOURCES  # do not overwrite

N_CYCLES = 500

averageDegree = 5  # default average degree

prop = 10.  # proportionality between P_s and P_a

P_a = float(averageDegree) / N_USERS  # do not overwrite
P_s = prop * P_a                      # do not overwrite

dim = 3  # state dimension

memorySize = 1  # memory dimension

overwrite = True  # sources overwrite old news when creating newer

verbose = False

projectVersion = 0.0  # useless

toBeExecuted = "print ('Goodbye')"  # useless


# during execution ##

# User -> activate
pActivation = 0.7  # probability of first activation of users

# User -> remember
tRemember = 0.9  # threshold above that a news is beautiful
pForget = 0.1  # probability to forget a news

# User -> readNews
vOld = 24  # value of an old news

# User -> becomeActive
tActivation = 7  # cutoff of inactivation
pActivation = 0.08  # probability of 'first' activation

# User -> becomeInactive
tInactivation = 2  # cutoff of activation
pInactivation = 0.08  # probability of 'first' activation

# User -> changeState
pChange = 0.5  # weight of changing state

# User -> activeDiffusion
pActiveDiffusion = 0.1  # probability to diffuse to a random neighbour
tActiveDiffusion = 0.1  # threshold between what influence the link
pWeight = 0.1  # weight of weight change
pRemove = 0.1  # value of weight below which there is rimotion

# User -> createEdge
tCreateEdge = 0.6  # threshold of random creation if the node is without connections

# User -> deleteEdge
pDeleteEdge = 0.1  # probability of removing a random edge

debug = True
