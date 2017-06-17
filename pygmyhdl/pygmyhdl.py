# -*- coding: utf-8 -*-

# MIT license
# 
# Copyright (C) 2017 by XESS Corp.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

import sys
import os
import re
import logging
from copy import deepcopy
from pprint import pprint
import pdb
from myhdl import *
from myhdlpeek import *
from random import randrange

logger = logging.getLogger('pygmyhdl')

USING_PYTHON2 = (sys.version_info.major == 2)
USING_PYTHON3 = not USING_PYTHON2

DEBUG_OVERVIEW = logging.DEBUG
DEBUG_DETAILED = logging.DEBUG - 1
DEBUG_OBSESSIVE = logging.DEBUG - 2


# List of MyHDL instances generated by this module.
_instances = list()
_wire_setters = list()

def initialize():
    global _instances, _wire_setters
    _instances = list()
    _wire_setters = list()
    Peeker.clear()

class Wire(SignalType):
    def __init__(self, name=None):
        super().__init__(bool(0))
        if name:
            Peeker(self, name)

class Bus(SignalType):
    def __init__(self, width=1, name=None):
        super().__init__(intbv(0, min=0, max=2**width))
        self.width = width
        self._wo_done = False
        if name:
            Peeker(self, name)

    @property
    def wo(self):
        if self._wo_done:
            return self.wires
        self.wires = [Wire() for _ in range(0, self.width)]
        @always_comb
        def set_wires():
            self.next = ConcatSignal(*reversed(self.wires))
        _wire_setters.append(set_wires)
        self._wo_done = True
        return self.wires

def simulate(*modules):
    def flatten(nested_list):
        lst = []
        for item in nested_list:
            if isinstance(item, (list, tuple)):
                lst.extend(flatten(item))
            else:
                lst.append(item)
        return lst

    modules = set(flatten(modules))
    for m in modules:
        if m in _instances:
            #instances = list(set([*modules, *_wire_setters, *Peeker.instances()]))
            #Simulation(*instances)
            Simulation(*modules, *_wire_setters, *Peeker.instances()).run()
            return
    #instances = list(set([*modules, *_instances, *_wire_setters, *Peeker.instances()]))
    #Simulation(*instances)
    Simulation(*modules, *_instances, *_wire_setters, *Peeker.instances()).run()

def get_max(signal):
    return signal.max or 2**len(signal)

def get_min(signal):
    return signal.min or 0

def random_test(num_tests, *wires):
    for _ in range(num_tests):
        for wire in wires:
            wire.next = randrange(get_min(wire), get_max(wire))
        yield delay(1)
    
def exhaustive_test(*wires):
    if len(wires) == 0:
        yield delay(1)
    else:
        for wires[0].next in range(get_min(wires[0]), get_max(wires[0])):
            yield from exhaustive_test(*wires[1:])

def random_sim(num_steps, *wires):
    simulate(random_test(num_steps, *wires))

def exhaustive_sim(*wires):
    simulate(exhaustive_test(*wires))

show_waveforms = Peeker.to_wavedrom

def group(f):
    def group_wrapper(*args, **kwargs):
        begin = len(_instances)
        f(*args, **kwargs)
        return _instances[begin:]
    return group_wrapper

# def group(f):
    # def blk_wrapper(*args, **kwargs):
        # blk = block(f)
        # return blk(*args, **kwargs)
    # def grp_wrapper(*args, **kwargs):
        # begin = len(_instances)
        # blk = blk_wrapper(*args, **kwargs)
        # _instances.extend(blk)
        # return _instances[begin:]
    # return grp_wrapper

# def group(f):
    # def wrapper(*args, **kwargs):
        # begin = len(_instances)
        # f(*args, **kwargs)
        # return _instances[begin:] 
    # wrapper = block(wrapper)
    # def wrapper2(*args, **kwargs):
        # blk = wrapper(*args, **kwargs)
        # _instances.append(blk)
        # return blk
    # return wrapper2


############## Logic gate definitions. #################

@block
def and_g(a, b, c):
    @always_comb
    def logic():
        c.next = a & b
    _instances.append(logic)
    return logic

@block
def or_g(a, b, c):
    @always_comb
    def logic():
        c.next = a | b
    _instances.append(logic)
    return logic

@block
def xor_g(a, b, c):
    @always_comb
    def logic():
        c.next = a ^ b
    _instances.append(logic)
    return logic
