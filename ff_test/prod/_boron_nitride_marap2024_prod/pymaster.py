import os
import sys
import ast
import numpy as np
import math as m
import copy as cp
import json
from pymodule import GetFullPath, GetDirName, Generate, ParseBasis, Run
from pypost_proc import PostProc

kGenerate = True
kRun      = True
kRead     = True
kPostProc = True

if kRead:
  # Read the parameters
  file_parameter = '_boron_nitride_marap2024_thesis.json'
  with open('parameter/' + file_parameter) as foo:
    pp = json.load(foo)
else:
  # Custom parameters
  print()

for key in pp:
  print('  ', key, pp[key])

if kGenerate: Generate(pp)
if kRun:      Run(pp)
if kPostProc: PostProc(pp)
