"""

coloroutput

"""

try:
    from colorama import init, Fore, Back
    init(autoreset=True)
    DEBUG_LABEL = "[ " + Fore.BLACK + Back.YELLOW + "DEBUG" + Fore.RESET + Back.RESET + " ] "
    LOG_LABEL = "[ " + Fore.YELLOW + "LOG" + Fore.RESET + " ] "  # [ LOG ]
    OK_LABEL = "[ " + Fore.GREEN + "OK" + Fore.RESET + " ] "  # [ OK ]
    INPUT_LABEL = "[ " + Fore.BLACK + Back.WHITE + " INPUT " + Fore.RESET + Back.RESET + " ] "
    WARNING_MSG = Fore.YELLOW
    ERROR_MSG = Fore.RED
except ImportError:
    DEBUG_LABEL = "[ DEBUG ] "  # [ LOG ]
    LOG_LABEL = "[ LOG ] "  # [ LOG ]
    OK_LABEL = "[ OK ] "  # [ OK ]
    INPUT_LABEL = "[ INPUT ] "
    WARNING_MSG = "[ WARNING ] "
    ERROR_MSG = "[ ERROR ] "
