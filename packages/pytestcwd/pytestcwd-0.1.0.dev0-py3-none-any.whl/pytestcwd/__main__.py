import os
import sys


import pytest


def console_script_entry():
    sys.path.insert(0, os.getcwd())
    pytest.main(sys.argv[1:])
    pass


if __name__ == '__main__':
    console_script_entry()
