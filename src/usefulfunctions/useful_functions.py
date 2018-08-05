import commonVar as common
import sys
import csv

def vprint(*args, sep=' ', end='\n', file=None):
    """

    print only if common.verbose = True

    """

    if common.verbose is True:
        print(*args, sep=' ', end='\n', file=None)


def digit_input(msg="Enter a number: ", DEFAULT=0):
    """
        prompt the user for a numeric input
        prompt again if the input is not numeric
        return an integer or a float
    """

    while True:
        # strip() removes any leading or trailing whitespace
        num_str = input(msg).strip()
        if len(num_str) == 0:
            return DEFAULT
        # make sure that all char can be in a typical number
        if all(c in '+-.0123456789' for c in num_str):
            break
        else:
            return DEFAULT
        # a float contains a period (US)
    if '.' in num_str:
        return float(num_str)
    else:
        return int(num_str)


def worldAgentStringsizer(agent):
    """

    Can convert an agent into a string

    """

    return str({
        'state': agent.state,
        'type': agent.agType,
        'database': agent.database
    })


def singleNewsStringsizer(agent):
    """

    print the memory of the agent

    """

    return str([agent.database[key]['id-n'] for key in agent.database])

def printHeader(w = csv.writer(open("temp.txt", "w")), firstline="#FIRST_LINE", lastline="#LAST_LINE"):
    w.writerow(firstline)
    w.writerow(['#'])
    w.writerow(['#simulation with:', common.N_CYCLES])
    w.writerow(['#SEED', common.SEED])
    w.writerow(['#N_AGENTS', common.N_AGENTS])
    w.writerow(['#N_USERS', common.N_USERS])
    w.writerow(['#N_SOURCES', common.N_SOURCES])
    w.writerow(['#P_a', common.P_a])
    w.writerow(['#P_s', common.P_s])
    w.writerow(['#dim', common.dim])
    w.writerow(['#time', common.localtime])
    w.writerow(['#memorySize', common.memorySize])
    w.writerow(lastline)

def hill(x, p, k, n):
    return ( -0.5 +( 1 / (1 + (k/x)**n)) ) * (1-p)*2 + p
