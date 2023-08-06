# encoding: utf8
"""Load lp file knowing its path.

"""
from functools import partial

NAME = 'Open lp file'
TAGS = {'ASP', 'utils'}


INPUTS = {}
OUTPUTS = {}  # in fact, we do not know. Sorry.

def run_on(context:str, *, file:open=None):
    """
    file -- the lp file to open. Must contains valid ASP.
    """
    if file:
        with open(file) as fd:
            yield fd.read()
