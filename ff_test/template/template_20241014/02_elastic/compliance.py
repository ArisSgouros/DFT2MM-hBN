#!/usr/bin/env python

# This file reads in the file log.lammps generated by the script ELASTIC/in.elastic
# It prints out the 6x6 tensor of elastic constants Cij
# followed by the 6x6 tensor of compliance constants Sij
# It uses the same conventions as described in:
# Sprik, Impey and Klein PRB (1984).
# The units of Cij are whatever was used in log.lammps (usually GPa)
# The units of Sij are the inverse of that (usually 1/GPa)

from __future__ import print_function
from numpy import zeros
from numpy.linalg import inv
import sys
import json

# parse the z component of the basis from the command line
az = float(sys.argv[1]) # [Angstrom]
kAngstromToMeterPerGiga = 1e-10*1e9

# define logfile layout

nvals = 21
valpos = 4
valstr = '\nElastic Constant C'

# define order of Cij in logfile

cindices = [0]*nvals
cindices[0] = (0,0)
cindices[1] = (1,1)
cindices[2] = (2,2)
cindices[3] = (0,1)
cindices[4] = (0,2)
cindices[5] = (1,2)
cindices[6] = (3,3)
cindices[7] = (4,4)
cindices[8] = (5,5)
cindices[9] = (0,3)
cindices[10] = (0,4)
cindices[11] = (0,5)
cindices[12] = (1,3)
cindices[13] = (1,4)
cindices[14] = (1,5)
cindices[15] = (2,3)
cindices[16] = (2,4)
cindices[17] = (2,5)
cindices[18] = (3,4)
cindices[19] = (3,5)
cindices[20] = (4,5)

# open logfile

with open("log.lammps",'r') as logfile:
    txt = logfile.read()

# search for 21 elastic constants

c = zeros((6,6))
s2 = 0

for ival in range(nvals):
    s1 = txt.find(valstr,s2)
    if (s1 == -1):
        print("Failed to find elastic constants in log file")
        exit(1)
    s1 += 1
    s2 = txt.find("\n",s1)
    line = txt[s1:s2]
#    print line
    words = line.split()
    (i1,i2) = cindices[ival]
    c[i1,i2] = float(words[valpos])
    c[i2,i1] = c[i1,i2]


# convert GPa to Pa*m
for i in range(6):
    for j in range(6):
        c[i][j] *= az*kAngstromToMeterPerGiga

print("C tensor [Pa m]")
for i in range(6):
    for j in range(6):
        print("%10.8g " % c[i][j], end="")
    print()

# export to json
cc = {'c11': c[0][0], 'c22': c[1][1],'c66': c[5][5],'c26': c[1][5],'c16': c[0][5],'c12': c[0][1]}
with open('o.elastic_stiffness.json', 'w') as foo: 
    json.dump(cc, foo)

# apply factor of 2 to columns of off-diagonal elements

for i in range(6):
    for j in range(3,6):
        c[i][j] *= 2.0

s = inv(c)

# apply factor of 1/2 to columns of off-diagonal elements

for i in range(6):
    for j in range(3,6):
        s[i][j] *= 0.5

print("S tensor [1/(Pa m)]")
for i in range(6):
    for j in range(6):
        print("%10.8g " % s[i][j], end="")
    print()

# export to json
ss = {'s11': s[0][0], 's22': s[1][1],'s66': s[5][5],'s26': s[1][5],'s16': s[0][5],'s12': s[0][1]}
with open('o.elastic_compliance.json', 'w') as foo: 
    json.dump(ss, foo)
