import commonVar as common


def vprint(*args, sep=' ', end='\n', file=None):
    if common.verbose is True:
        print(*args, sep=' ', end='\n', file=None)


def digit_input(DEFAULT=1, msg=""):
    """

    takes an input and controls if it is emplty or a string

    DEFAULT: the default value returned if errors

    msg: the input message

    """

    input_str = input(msg)
    if len(input_str) == 0:
        pass
    elif not input_str.isdigit():
        pass
    else:
        try:
            DEFAULT = eval(input_str)
        except ValueError:
            pass
    return DEFAULT
