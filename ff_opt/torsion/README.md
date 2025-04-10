# Opt torsion
Optimization of the torsional potential by bending the sheet along the ZZ or AC directions

# Description
This folder contains the source code for biaxial strain calculations of BN monolayers.

# Organization
The folder includes the following files and directories:
 - README.md -> current file
 - BN_ac_dih_0.in -> Quantum Espresso input file for BN bended along the AC direction.
 - BN_ac_dih_0.out -> Quantum Espresso output file for BN bended along the AC direction.
 - BN_zz_dih_0.in -> Quantum Espresso input file for BN bended along the ZZ direction.
 - BN_zz_dih_0.out -> Quantum Espresso output file for BN bended along the ZZ direction.
 - hBNArmchair.script -> Bash script for generating BN bended along the AC direction.
 - hBNZigZag.script -> Bash script for generating BN bended along the ZZ direction.
 - torsion_energy.csv -> CSV with potential energy as function of bending angle
 - fit_torsion.py -> Python script for fitting the torsional terms
 - fit_torsion.log -> Log of the python optimization
 - fit_torsion.xlsx -> Excel file for visualizing the energetic components and fitting
