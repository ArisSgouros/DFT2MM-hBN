import numpy as np
import sys

dim2int = {'x':0, 'y':1, 'z':2}

def CntRadius(filename, dim1, dim2):

  dim1 = dim2int[dim1]
  dim2 = dim2int[dim2]
  lbox = [0.0,0.0,0.0]

  with open(filename) as foo:
    lines = foo.readlines()

  for ii in range(len(lines)):
    line = lines[ii]

    if "atoms" in line:
      natom = int(line.split()[0])
    if "Atoms" in line:
      line_Atoms = ii + 2
    if "xlo xhi" in line:
      lbox[0] = float(line.split()[1])-float(line.split()[0])
    if "ylo yhi" in line:
      lbox[1] = float(line.split()[1])-float(line.split()[0])
    if "zlo zhi" in line:
      lbox[2] = float(line.split()[1])-float(line.split()[0])

  # Read atom section
  rrs = [None for ii in range(natom)]

  for ii in range(natom):
    line_split = lines[line_Atoms + ii].split()
    idx = int(line_split[0])
    xx  = float(line_split[4])+int(line_split[7])*lbox[0]
    yy  = float(line_split[5])+int(line_split[8])*lbox[1]
    zz  = float(line_split[6])+int(line_split[9])*lbox[2]
    rrs[idx-1] = np.array([xx, yy, zz])

  r1_ref = 0.0
  r2_ref = 0.0
  for rr in rrs:
    r1_ref += rr[dim1]
    r2_ref += rr[dim2]
  r1_ref/=natom
  r2_ref/=natom

  
  radius = 0.0
  for rr in rrs:
    radius = np.sqrt((rr[dim1]-r1_ref)**2 + (rr[dim2]-r2_ref)**2)

  return radius


if __name__ == "__main__":
   file_in = sys.argv[1]
   dim1 = sys.argv[2]
   dim2 = sys.argv[3]
   print(file_in)
   print(dim1)
   print(dim2)
   print(CntRadius(file_in,dim1,dim2))
