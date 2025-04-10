import numpy as np
import os
import sys
import json
import scipy.optimize as opt

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

iter = 0
def ObjFun(xx, target_pxx, target_pyy, path_lammps):

    # run the minimization
    cmd = "%s -in in.box_relax -v LX %.15e -v LY %.15e > o.log.lammps" % (path_lammps, xx[0], xx[1])
    os.system(cmd)

    # Read the thermodynamics of the minimized configuration
    dthermo = ReadThermo("o.box_relax_thermo")

    current_pxx = dthermo["pxx"]
    current_pyy = dthermo["pyy"]

    # Calculate the error between the target and current value
    merit = pow(current_pxx - target_pxx, 2) \
          + pow(current_pyy - target_pyy, 2)

    # Report the progress
    global iter
    print("%15d %.15e %.15e %.15e %.15e %.15e" % (iter, merit, xx[0], xx[1], current_pxx, current_pyy))
    iter += 1

    return merit

if __name__ == "__main__":

  # Read the parameters
  with open('../i.parameter.json') as foo:
    pp = json.load(foo)

  path_crystal_builder = pp['path_crystal_builder']+'/'+'crystal_builder.py'
  path_basis = pp['path_basis']
  path_lammps = pp['path_lammps']
  nx, ny, nz = pp['sheet_ni']
  crystal_builder_option = pp['crystal_builder_option']

  file_pos  = "o.pos.dat"
  file_dump = "o.dump.lammpstrj"
  file_log  = "o.log.lammps"

  cmd = "python %s %s \"%s,%s,%s\" --file_pos=%s --file_dump=%s %s > %s" % (path_crystal_builder, path_basis, nx, ny, nz, file_pos, file_dump, crystal_builder_option, file_log)
  os.system(cmd)

  # Minimization section
  print("# Optimize box dimensions for zero lateral pressure..")

  # Set the target pressure tensor
  target_pxx = 0.0
  target_pyy = 0.0

  print("%15s %15s %15s %15s %15s %15s" % ("step", "merit", "lx", "ly", "pxx", "pyy"))

  # set initial guess
  lx0 = nx*pp['basis_ax']
  ly0 = ny*pp['basis_ay']
  res = opt.minimize(ObjFun, np.array([lx0, ly0]), args=(target_pxx, target_pyy, path_lammps, ), method='nelder-mead',tol=1e-14,options={'disp': True})

  print("Coeffs   : ", res.x)
  print("Residual : ", ObjFun(res.x, target_pxx, target_pyy, path_lammps))
  dthermo = ReadThermo("o.box_relax_thermo")
  dthermo['area_density'] = float(dthermo['atoms']) / (float(dthermo['lx'])*float(dthermo['ly']))
  dthermo['basis_ax_opt'] = float(dthermo['lx']) / nx
  dthermo['basis_ay_opt'] = float(dthermo['ly']) / ny
  with open('../o.box_relax.json', 'w') as foo:
    json.dump(dthermo, foo)

  # Export optimized basis files
  cmd = "python %s/DatafileDeform/datafile_deform.py ../i.basis -atomtype=\"full\" -xhi=%f -yhi=%f > ../i.basis_opt" % (pp["path_lmp_tool"], dthermo['basis_ax_opt'], dthermo['basis_ay_opt'])
  os.system(cmd)

  cmd = "python %s/DatafileDeform/datafile_deform.py ../i.basis_transpose -atomtype=\"full\" -xhi=%f -yhi=%f > ../i.basis_transpose_opt" % (pp["path_lmp_tool"], dthermo['basis_ay_opt'], dthermo['basis_ax_opt'])
  os.system(cmd)

  if not res.success:
    print("Optimization not converged!")
