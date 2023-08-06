#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ********************************************************************************************
# imports
import time
from typing import Dict

# custom libraries
import BiofilmSimulation.constants as constants


# ********************************************************************************************
# Utility functions

def simulation_duration(func):
    def inner1(*args, **kwargs):
        # storing time before function execution
        begin = time.time()
        func(*args, **kwargs)
        # storing time after function execution
        end = time.time()
        print(f'Duration of {func.__name__} : {end - begin} s')

    return inner1


def prompt_log_at_start(constant: constants):
    """ Log printed in terminal at start """
    print(f" ************ BIOFILM MODELING ************ \n"
          " A project of the iGEM Teams Hannover x Darmstadt\n")
    print(constant)


def print_dic(dic: Dict):
    for key, item in dic.items():
        print(f"  {key} :  {item}")
