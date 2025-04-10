import numpy as np
import os
import sys
import json
import scipy.optimize as opt
import copy as cp
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

if __name__ == "__main__":

  # Read the parameters
  with open('../i.parameter.json') as foo:
    pp = json.load(foo)

  path_crystal_builder = pp['path_crystal_builder']+'/'+'crystal_builder.py'
  path_lammps = pp['path_lammps']
  path_basis = pp['path_basis']
  sheet_nx, sheet_ny, sheet_nz = pp['sheet_ni']
  path_sheet_to_cnt = pp['path_sheet_to_cnt']
  crystal_builder_option = pp['crystal_builder_option']
  iter_cnt = pp['iter_cnt']

  # Parse the peratom energy from 01_box_relax
  with open('../o.box_relax.json') as foo:
    dthermo_sheet = json.load(foo)

  basis_ax = dthermo_sheet['basis_ax_opt']
  basis_ay = dthermo_sheet['basis_ay_opt']

  path_csv = "../o.nanotube.csv"


  # Generate csv header
  flog = open(path_csv,"w")
  flog.write("%s,%s,%s,%s,%s," % ("dim", "nx", "ny", "merit", "radius",))
  dthermo = ReadThermo("i.log_header")
  for key in dthermo:
    flog.write("%s," % (key))
  flog.write("\n")
  
  n_list          = pp['nanotube_ni']
  path_basis_dim  = {'x': '../i.basis_opt'        , 'y': '../i.basis_transpose_opt'}
  ny_norm_dim     = {'x': sheet_ny                , 'y': sheet_nx}
  box_norm_init_dim     = {'x': float(sheet_ny)*basis_ay, 'y':  float(sheet_nx)*basis_ax}

  for dim in ['x','y']:
    path_basis = path_basis_dim[dim]
    ny_norm    = ny_norm_dim[dim]
    box_norm         = box_norm_init_dim[dim]

    # Set initial condition
    for nx_cnt in n_list[dim]:

      print("Case: dim=%s, nx_cnt=%s, ny_norm=%s" %(dim, nx_cnt, ny_norm))

      print("# Generate a sheet..")
      file_tag = "o.%s_%d_%d" % (dim, nx_cnt, ny_norm)
      file_pos_sheet = file_tag + "_sheet.dat"
      file_log = file_tag + "_sheet.log"

      cmd = "python %s %s \"%s,%s,%s\" --file_pos=%s --file_dump=%s %s > %s" % (path_crystal_builder, path_basis, nx_cnt, ny_norm, sheet_nz, file_pos_sheet, file_tag+"_sheet.lammpstrj", crystal_builder_option, file_log)
      os.system(cmd)

      print("# Roll sheet into a CNT..")
      file_pos_cnt = file_tag + "_cnt.dat"
      cmd = "python %s %s -data_file_out=%s -dim_roll=%s -dim_norm=%s > o.log_sheet_to_cnt" % (path_sheet_to_cnt, file_pos_sheet, file_pos_cnt, 'x', 'z')
      os.system(cmd)

      # Minimization section
      print("# Optimize CNT length for zero uniaxial pressure..")
      file_pos_emin = "pos_emin.dat"
      os.system("cp " + file_pos_cnt + " " + file_pos_emin)

      # Set the target pressure tensor
      target_pyy = 0.0

      print("%15s %15s %15s %15s " % ("step", "merit", "box_norm", "press_norm"))

      iter = 0
      def Obj(xx, target_pyy):

        # run the minimization
        cmd = "%s -in in.relax_box_norm -v box_norm %.15e > log.emin_all" % (path_lammps, xx)
        os.system(cmd)

        # Read the thermodynamics of the minimized configuration
        dthermo = ReadThermo("o.log.press")

        current_pyy = dthermo["pyy"]

        # Calculate the error between the target and current value
        merit = pow(current_pyy - target_pyy, 2)

        # Report the progress
        global iter
        print("%15d %.15e %.15e %.15e" % (iter, merit, xx, current_pyy))
        iter += 1

        return merit

      # reevaluate the optimized parameter set
      merit = 0.0
      if iter_cnt > 1:
        res = opt.brent(Obj, args=(target_pyy, ), brack=(box_norm*0.99,box_norm*1.01), tol=1.e-12, full_output=1, maxiter=iter_cnt)
        box_norm = res[0]
        merit = res[1]
      Obj(box_norm, target_pyy)

      os.system("mv dump.lammpstrj " + file_tag + "_cnt.lammpstrj")
      os.system("mv pos_emin_final.dat " + file_pos_cnt)
      os.system("mv log.emin_all " + file_pos_cnt + "_log_emin")

      #
      # Calculation of np radius (numerical)
      r_np = CntRadius(file_pos_cnt, 'x', 'z')
      print("# Radius: %f" %r_np)

      # export the thermo quantities
      dthermo = ReadThermo("o.log.press")
      flog.write("%s,%d,%d,%f,%.15e," % (dim, nx_cnt, ny_norm, merit, r_np))
      for key in dthermo:
        flog.write("%.15e," % (dthermo[key]))
      flog.write("\n")

  flog.close()
