import numpy as np
import os
import sys
import json
import scipy.optimize as opt
from pyradius import CntRadius

def ReadThermo(filename):
   o_file = open(filename)
   line = o_file.readline().split()
   o_file.close()
   dthermo = {}
   for ii in range(0, len(line), 2):
      key = line[ii]
      val = float(line[ii+1])
      dthermo[key] = val
   return dthermo

def KeyOfList(xx):
  return '_'.join(xx)

if __name__ == "__main__":

  # Read the parameters
  with open('../i.parameter.json') as foo:
    pp = json.load(foo)

  path_crystal_builder = pp['path_crystal_builder']+'/'+'crystal_builder.py'
  path_lammps = pp['path_lammps']
  path_sheet_to_cnt = pp['path_sheet_to_cnt']
  path_crystal_builder = pp['path_crystal_builder']+'/'+'crystal_builder.py'
  crystal_builder_option = pp['crystal_builder_option']

  path_csv = "../o.torus.csv"

  n_list          = pp['torus_ni']
  path_basis_dim  = {'x': '../i.basis_opt'   , 'y': '../i.basis_transpose_opt'}

  # Generate csv header
  flog = open(path_csv,"w")
  flog.write("%s,%s,%s,%s," % ("dim", "nx", "ny", "radius"))
  dthermo = ReadThermo("i.log_header")
  for key in dthermo:
    flog.write("%s," % (key))
  flog.write("\n")

  for dim in ['x', 'y']:
    path_basis = path_basis_dim[dim]

    for nx, ny in n_list[dim]:

      print("Case: dim=%s, nx=%s, ny=%s" %(dim, nx, ny))

      file_tag = "o.%s_%d_%d" % (dim, nx, ny)
      file_pos_sheet = file_tag + "_sheet.dat"
      file_pos_cnt = file_tag + "_cnt.dat"
      file_pos_torus = file_tag + "_torus.dat"
      file_log = file_tag + "_sheet.log"
      file_log_thermo = file_tag + "_torus.log"

      if os.path.isfile(file_pos_sheet):
         print("  Skip existing case.. ")
      else:

        print("# Generate a sheet..")
        cmd = "python %s %s \"%s,%s,%s\" --file_pos=%s --file_dump=%s %s > %s" % (path_crystal_builder, path_basis, nx, ny, 1, file_pos_sheet, file_tag+"_sheet.lammpstrj", crystal_builder_option, file_log)
        os.system(cmd)

        print("# Roll sheet into a CNT..")
        cmd = "python %s %s -data_file_out=%s -dim_roll=%s -dim_norm=%s > o.log_sheet_to_cnt" % (path_sheet_to_cnt, file_pos_sheet, file_pos_cnt, 'x', 'z')
        os.system(cmd)

        print("# Roll CNT into a torus")
        cmd = "python %s %s -data_file_out=%s -dim_roll=%s -dim_norm=%s > o.log_cnt_to_torus" % (path_sheet_to_cnt, file_pos_cnt, file_pos_torus, 'y', 'z')
        os.system(cmd)

        # run the minimization
        file_pos_emin = "pos_emin.dat"
        os.system("cp " + file_pos_torus + " " + file_pos_emin)
        cmd = path_lammps + " -in " + "in.relax > log.relax"
        os.system(cmd)

        os.system("mv dump.lammpstrj " + file_tag + "_torus.lammpstrj")
        os.system("mv pos_emin_final.dat " + file_pos_torus)
        os.system("cp o.log_thermo " + file_tag + "_torus.log")
        os.system("cp log.lammps " + file_tag + "_torus.loglmp")

      dthermo = ReadThermo(file_log_thermo)

      print("# Calculate torus radius..")
      r_torus = CntRadius(file_pos_torus, 'y', 'z')


      # export the thermo quantities
      flog.write("%s,%d,%d,%.15e," % (dim, nx, ny, r_torus))
      for key in dthermo:
        flog.write("%.15e," % (dthermo[key]))
      flog.write("\n")
  flog.close()
