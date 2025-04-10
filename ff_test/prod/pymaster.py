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
kRead     = False
kPostProc = True

if kRead:
  # Read the parameters
  #file_parameter = '_aGDy_CH.airebo_test.json'
  #file_parameter = '_12-6-Gdy_CH.airebo_test/'
  #file_parameter = '_boron_nitride_intra2013-2017_test.json'
  file_parameter = '_graphene_CH.airebo_test.json'
  with open('parameter/' + file_parameter) as foo:
    pp = json.load(foo)
else:
  # Custom parameters
  pp = {}
  pp['system']      = 'boron_nitride_sphere'
  pp['basis']       = 'boron_nitride_orth_zz'
  pp['potential']   = 'marap2024'
  pp['template']    = 'template_20241014'
  pp['comment']     = 'test'
  pp['simulation']  = ['01_box_relax', '02_elastic', '03_nanotube']
  pp['sheet_ni']    = [4, 2, 1]
  pp['nanotube_ni'] = {'x': [5], \
                       'y': [3]}
  pp['crystal_builder_option'] = "--rc=1.4518 --bond=1 --angle=1 --dihed=1 --cis_trans=1 --grid=\"xy\""

  pp['path_lammps']    = 'lmp_mpi'
  pp['path_current']   = GetFullPath('.') + '/'
  pp['path_master']    = GetFullPath('../') + '/'
  pp['path_template']  = pp['path_master'] + 'template/'  + pp['template']
  pp['path_basis']     = pp['path_master'] + 'basis/'     + pp['basis']
  pp['path_potential'] = pp['path_master'] + 'potential/' + pp['potential']
  pp['path_crystal_builder'] = GetFullPath('~/Programs/CrystalBuilder/') + '/'
  pp['path_sheet_to_cnt'] = "/home/asgouros/Programs/LmpTool/SheetToCnt/sheet_to_cnt.py"
  pp['path_lmp_tool'] = "/home/asgouros/Programs/LmpTool/"

  basis_atom, basis_ax, basis_ay, basis_az = ParseBasis(pp['path_basis'])
  if basis_atom is None or basis_ax is None or basis_ay is None:
    print("Error with parsing basis %s" % (pp['path_basis']))
  pp['basis_atom'] = basis_atom
  pp['basis_ax'] = basis_ax
  pp['basis_ay'] = basis_ay
  pp['basis_az'] = basis_az
  pp['iter_cnt'] = 0

for key in pp:
  print('  ', key, pp[key])

if kGenerate: Generate(pp)
if kRun:      Run(pp)
if kPostProc: PostProc(pp)
