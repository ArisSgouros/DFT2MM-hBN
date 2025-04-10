import os
import sys
import json
import numpy as np
import collections
import subprocess

def ParseBasis(path_basis):
   basis_atom = None
   basis_ax = None
   basis_ay = None
   with open(path_basis, 'r') as foo:
      lines = foo.readlines()
   for line in lines:
      if 'atoms' in line:
         data = line.split()
         basis_atom = int(data[0])
      if ('xlo' in line) and ('xhi' in line):
         data = line.split()
         basis_ax = float(data[1]) - float(data[0])
      if ('ylo' in line) and ('yhi' in line):
         data = line.split()
         basis_ay = float(data[1]) - float(data[0])
      if ('zlo' in line) and ('zhi' in line):
         data = line.split()
         basis_az = float(data[1]) - float(data[0])
   return basis_atom, basis_ax, basis_ay, basis_az

def GetLinesOfFileThatIncludesString(string, file):
   lines = []
   foo = open(file, 'r')
   file_lines = foo.readlines()
   for line in file_lines:
      if string in line:
         lines.append(line)
   return lines

def GetFullPath(dir):
    cmd = "readlink -f " + dir
    output = subprocess.getoutput(cmd)
    return output

def ExportDict(path):
   unord_dict = {}
   foo = open(path, "r")
   while True:
      line = foo.readline();
      if len(line) == 0: break # EOF
      line_split = line.split()
      unord_dict[line_split[0]] = line_split[1]
   ord_dict = collections.OrderedDict(sorted(unord_dict.items()))
   return ord_dict

def ImportDict(path):
   unord_dict = {}
   foo = open(path, "r")
   while True:
      line = foo.readline();
      if len(line) == 0: break # EOF
      line_split = line.split()
      unord_dict[line_split[0]] = line_split[1]
   ord_dict = collections.OrderedDict(sorted(unord_dict.items()))
   return ord_dict

def GetDirName(pp):
   dir  = ""
   dir += '_%s'   % str(pp['system'])
   dir += '_%s'   % str(pp['potential'])
   dir += '_%s'   % str(pp['comment'])
   return dir

def Run(pp):
   path_dir = GetDirName(pp) + '/'
   if not os.path.exists(path_dir):
     print("skip:   ",path_dir)
     return

   # relax box dimensions
   for sim in pp['simulation']:
      os.chdir(path_dir + '/' + sim)
      os.system('python pyrun.py')
      os.chdir(pp['path_current'])
   return

def Generate(pp):

   # generate the simulation folder
   name_dir = GetDirName(pp)
   path_dir = name_dir + '/'
   if (os.path.exists(path_dir)):
     print("skip:   ",path_dir)
     return
   else:
     print("create: ",path_dir)
   os.system('cp -r %s %s' % (pp['path_template'], path_dir))

   # make a copy of pymaster within
   os.system('cp -r pymaster.py %s/.' % (path_dir))

   # store the simulation parameters
   path_parameter = "%s/%s" % (path_dir, 'i.parameter.json')
   with open(path_parameter, 'w') as foo: 
      json.dump(pp, foo)
   path_parameter = "parameter/%s.json" % (name_dir)
   with open(path_parameter, 'w') as foo: 
      json.dump(pp, foo)

   # import potential, basis and basis (transported)
   os.system('cp -r %s/* %s'         % (pp['path_potential'], path_dir))
   os.system('cp    %s   %s/i.basis' % (pp['path_basis'], path_dir))
   path_datafile_transport = "%s/DatafileTranspose/datafile_transpose.py" % (pp['path_lmp_tool'])
   os.system("python %s %s/i.basis y x z > %s/i.basis_transpose " %(path_datafile_transport, path_dir, path_dir))
   return
