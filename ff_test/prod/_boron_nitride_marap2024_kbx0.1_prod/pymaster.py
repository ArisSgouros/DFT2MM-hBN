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
  file_parameter = '_boron_nitride_marap2024_kbx0.1_prod.json'
  with open('parameter/' + file_parameter) as foo:
    pp = json.load(foo)
else:
  # Custom parameters
  pp = {}
  pp['system']      = '12-6-Gdy'
  pp['basis']       = 'aGDy'
  pp['potential']   = 'CH.rebo'
  pp['template']    = 'template_20240825'
  pp['comment']     = 'prod'
  pp['simulation']  = ['01_box_relax', '02_elastic', '03_nanotube']
  pp['sheet_ni']    = [4, 8, 1]
  pp['nanotube_ni'] = {'x': [21,23,27,32,43,76], \
                       'y': [12,14,16,19,25,44]}
  pp['crystal_builder_option'] = "--rc=0.0 --bond=0 --angle=0 --dihed=0 --cis_trans=0 --grid=\"xy\""

  pp['path_lammps']    = 'lmp_mpi'
  pp['path_current']   = GetFullPath('.') + '/'
  pp['path_master']    = GetFullPath('../') + '/'
  pp['path_template']  = pp['path_master'] + 'template/'  + pp['template']
  pp['path_basis']     = pp['path_master'] + 'basis/'     + pp['basis']
  pp['path_potential'] = pp['path_master'] + 'potential/' + pp['potential']
  pp['path_crystal_builder'] = GetFullPath('~/Programs/CrystalBuilder/') + '/'
  pp['path_sheet_to_cnt'] = "/home/aps/Programs/LmpTool/SheetToCnt/sheet_to_cnt.py"
  pp['path_lmp_tool'] = "/home/aps/Programs/LmpTool/"

  basis_atom, basis_ax, basis_ay, basis_az = ParseBasis(pp['path_basis'])
  if basis_atom is None or basis_ax is None or basis_ay is None:
    print("Error with parsing basis %s" % (pp['path_basis']))
  pp['basis_atom'] = basis_atom
  pp['basis_ax'] = basis_ax
  pp['basis_ay'] = basis_ay
  pp['basis_az'] = basis_az

for key in pp:
  print('  ', key, pp[key])

if kGenerate: Generate(pp)
if kRun:      Run(pp)
if kPostProc: PostProc(pp)
