import os
import sys
import json
import numpy as np
import collections
import subprocess
import csv
from pymodule import GetDirName

def Code(coeff):
   return '_'.join(str(ii) for ii in coeff)


def PostProc(pp):
   path_dir = GetDirName(pp) + '/'
   if not os.path.exists(path_dir):
     print("skip:   ",path_dir)
     return

   # enter folder
   os.chdir(path_dir)

   with open('o.box_relax.json') as foo:
     pp_sheet = json.load(foo)

   sheet_pe_atom = pp_sheet['pe_atom']
   sheet_atoms = pp_sheet['atoms']
   sheet_lx = pp_sheet['lx']
   sheet_ly = pp_sheet['ly']
   sheet_density = sheet_atoms/(sheet_lx*sheet_ly)

   print('Sheet:')
   print('   pe/atom:', sheet_pe_atom)
   print('   density:', sheet_density)

   if "03_nanotube" in pp['simulation']:
      print('Nanotube:')
      with open('o.nanotube.csv', newline='\n') as csvin:
        with open('o.nanotube_proc.csv', 'w') as csvout:
          reader = csv.reader(csvin, delimiter=',', quotechar='|')
          writer = csv.writer(csvout)

          header = next(reader)
          header_add = ['code', 'pe_atom', 'pe_atom_ref', 'bm']
          writer.writerow(header_add + header)

          ntcol = {}
          for ii in range(len(header)):
            ntcol[header[ii]] = ii

          nt_data = {}
          for row in reader:
            nt_dim = row[ntcol['dim']]
            nt_nx = int(row[ntcol['nx']])
            nt_atoms = float(row[ntcol['atoms']])
            nt_radius = float(row[ntcol['radius']])
            nt_code = Code([nt_dim, nt_nx])
            nt_pe_atom = float(row[ntcol['pe_atom']])
            nt_pe_atom_ref = nt_pe_atom - sheet_pe_atom
            nt_bm = 2.0*sheet_density*nt_pe_atom_ref*nt_radius**2
            nt_data[nt_code] = {'dim': nt_dim, 'nx': nt_nx, 'radius': nt_radius, 'pe_atom': nt_pe_atom, 'pe_atom_ref': nt_pe_atom_ref, 'bm': nt_bm}

            row_add = [nt_code, nt_pe_atom, nt_pe_atom_ref,  nt_bm]

            writer.writerow(row_add + row)
            print(row_add)

      with open('o.nanotube_proc.json', 'w') as foo: 
        json.dump(nt_data, foo)


   if "04_torus" in pp['simulation']:
      print('Torus:')
      with open('o.torus.csv', newline='\n') as csvin:
        with open('o.torus_proc.csv', 'w') as csvout:
          reader = csv.reader(csvin, delimiter=',', quotechar='|')
          writer = csv.writer(csvout)

          header = next(reader)
          header_add = ['code', 'radius_ext', 'radius_int', 'pe_atom', 'pe_atom_ref']
          writer.writerow(header_add + header)

          trcol = {}
          for ii in range(len(header)):
            trcol[header[ii]] = ii


          tr_data = {}
          for row in reader:
            tr_dim = row[trcol['dim']]
            tr_nx = int(row[trcol['nx']])
            tr_ny = int(row[trcol['ny']])
            nt_code = Code([tr_dim, tr_nx])
            tr_code = Code([tr_dim, tr_nx, tr_ny])

            tr_radius_ext = float(row[trcol['radius']])
            tr_radius_int = nt_data[nt_code]['radius']
            tr_atoms = float(row[trcol['atoms']])
            tr_pe_atom = float(row[trcol['pe_atom']])
            tr_pe_atom_ref = tr_pe_atom - nt_data[nt_code]['pe_atom']

            tr_data[tr_code] = {'dim': tr_dim, 'nx': tr_nx, 'ny': tr_ny, 'radius_ext': tr_radius_ext, 'radius_int': tr_radius_int, 'pe_atom': tr_pe_atom, 'pe_atom_ref': tr_pe_atom_ref}

            row_add = [nt_code, tr_radius_ext, tr_radius_int, tr_pe_atom, tr_pe_atom_ref]

            writer.writerow(row_add + row)
            print(row_add)

        with open('o.torus_proc.json', 'w') as foo: 
           json.dump(tr_data, foo)


   os.chdir(pp['path_current'])
   return


