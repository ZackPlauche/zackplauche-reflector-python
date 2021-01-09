# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd
import re
from datetime import datetime
from pathlib import Path


def casefold_all(*vars) -> tuple:
    casefolded_vars_list = []
    for var in vars:
        if type(var) is str:
            casefolded_vars_list.append(var.casefold())
        elif type(var) in {list, tuple, set}:
            casefolded_vars_list.append(map(str.casefold, var))
    return tuple(casefolded_vars_list)

def get_datetime_now_vars():
    date = datetime.now().strftime('%#m/%#d/%Y')
    day = datetime.now().strftime('%A')
    time = datetime.now().strftime('%I:%H %p').lstrip('0').lower()
    return date, day, time

def debug(*args): 
    print('DEBUG: ', *args)