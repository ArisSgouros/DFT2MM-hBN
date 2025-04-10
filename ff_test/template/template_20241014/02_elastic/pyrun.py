import numpy as np
import os
import sys
import json

if __name__ == "__main__":

  # Read the parameters
  with open('../i.parameter.json') as foo:
    pp = json.load(foo)

  path_lammps = pp['path_lammps']

  # run the lammps script
  os.system("%s -in in.elastic -v up 1.0e-6 > o.log_1.0e-6.elastic" % (path_lammps))

  # compute the compliance and stiffness matrix 
  os.system("python compliance.py %f" % pp['basis_az'])

  # store stiffness
  os.system("cp o.elastic_stiffness.json o.elastic_stiffness_1.0e-6")

  # run the lammps script
  os.system("%s -in in.elastic -v up 1.0e-7 > o.log_1.0e-7.elastic" % (path_lammps))

  # compute the compliance and stiffness matrix 
  os.system("python compliance.py %f" % pp['basis_az'])

  # store stiffness
  os.system("cp o.elastic_stiffness.json o.elastic_stiffness_1.0e-7")
  os.system("cp o.elastic_stiffness.json ../.")
  os.system("cp o.elastic_compliance.json ../.")
