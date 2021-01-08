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

