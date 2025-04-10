# Prod
Calculate elastic properties of hBN nanostructures

# Description
This folder contains the source code and data from the molecular mechanics calculations. Additional details can be found in _boron_nitride_marap2024_prod/README.md

# Prerequisites
The following github repos are required:

  git@github.com:ArisSgouros/LmpTool.git
  git@github.com:ArisSgouros/CrystalBuilder.git

Replicating the results from scratch necesitates configuring the absolute paths in the i.parameter.json files.

# Usage
The workflow of the calculations can be inferred from the file pymaster.py and the associated modules.
Configuring properly the paths in the parameter files i.parameter.json, enables the replication of the whole data from scratch.

# Organization
 - README.md -> current file
 - basis/ -> Basis files
 - potential/ -> Potential files
 - prod/ -> Production code
 - template/ -> Templates
 - _boron_nitride_marap2024_prod/ -> Simulations using the default potential
 - _boron_nitride_marap2024_kbx0.1_prod/ -> Simulations using the potential with 10 times weaker in-plane angles
 - _boron_nitride_marap2024_kdx0.1_prod/ -> Simulations using the potential with 10 times weaker torsional angles
 - _boron_nitride_marap2024_kdx10_prod/ -> Simulations using the potential with 10 times stronger torsional angles
 - parameter/ -> Folder with parameter files used by pymaster.py
 - pymaster.py -> Schedule simulation steps based on the parameter files
 - pymodule.py -> Modules of pymaster.py
 - pypost_proc.py -> Post processing functions
 - pyprint.py -> Helper script which prints the parameters files
