import os, sys


def test_run():
    sys.path.append("../..")
    os.chdir("../../SLAPP3")
    os.system("python ./runShell.py")
