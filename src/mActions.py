import os
import sys

from Tools import *

from world.WorldAgent import *


def do0(address):  # reset in modelActions.txt
    self = address  # if necessary
    askEachAgentInCollection(address.agentList, WorldAgent.setNewCycleValues)


def do1(address):  # move in modelActions.txt
    self = address  # if necessary
    # set in each call to the group
    self.actionGroup1.setName("move")
    # set in each call to the group

    # keep safe the original list
    address.agentListCopy = address.agentList[:]
    # never in the same order (please comment if you want to keep
    # always the same sequence
    random.shuffle(address.agentListCopy)
    # move with a jump, to have to transfer a parameter
    # the format is: collection, method, parameters by name
    # ask each agent, without parameters
    # the potential jump is the same for all the agents

    # alternatively, we can pass the method as a str
    # (new way from v.1.36)
    """                                                               IMPORTANTE!!!!!!!!!!!!!!!
            askEachAgentInCollectionAndExecLocalCode \
                     (address.agentListCopy,"randomMovement",
                                        jump=random.uniform(0,5))
            """

    # or as an unbound method (the way used for v. <1.36)

    #askEachAgentInCollectionAndExecLocalCode \
    #         (address.agentListCopy,Agent.randomMovement,
    #                            jump=random.uniform(0,5))

    # the str way is preferred for agents subclassing Agent class
    # the other one is maintained for compatibility with
    # previous mActions.py files


# ptpt
def createTheAgent(self, line, num, agType):
    # explictly pass self, here we use a function

    if len(line.split()) == 1:
        anAgent = WorldAgent(num, self.worldState, agType=agType)
        self.agentList.append(anAgent)

    else:
        print("Error in file " + agType + ".txt")
        os.sys.exit(1)


# ptpt def createTheAgent_Class(self, line, num, leftX, rightX, bottomY,
# topY, agType, agClass):
def createTheAgent_Class(self, line, num, agType, agClass):
    # explictly pass self, here we use a function
    # print "leftX,rightX,bottomY,topY", leftX,rightX,bottomY,topY

    # loading classes with repetition (but only creating agents)
    # try:
    #    exec("from " + agClass + " import *")
    # except:
    # print "Class", agClass, "not found."
    # os.sys.exit(1)
    common.agClassVerified = False
    if not common.agClassVerified:
        try:
            exec("import " + agClass)
            common.agClassVerified = True
        except BaseException:
            print("Missing file " + agClass + ".py")
            os.sys.exit(1)

    agClassFile = agClass
    if agClass.find('.') >= 0:
        agClassFile = agClass.split('.')[-1]

    if len(line.split()) == 1:
        # try:
        # ptpt exec("anAgent = "+agClass+"(num,
        # self.worldState,random.randint(leftX,rightX),random.randint(bottomY,topY),leftX,rightX,bottomY,topY,agType=agType)")

        exec("from " + agClass + " import *;" + "anAgent = " + agClassFile +
             "(num, self.worldState,agType=agType)")
        self.agentList.append(locals()['anAgent'])
        # except:
        #    print
        #    print "Argument error creating an instance of class", agClass
        #    os.sys.exit(1)

    else:
        print("Error in file " + agType + ".txt")
        print("Error:", sys.exc_info()[0])
        os.sys.exit(1)


def otherSubSteps(subStep, address):
    return False
