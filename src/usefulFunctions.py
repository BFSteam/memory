import commonVar as common


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
