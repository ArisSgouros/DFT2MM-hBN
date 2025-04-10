# boron_nitride_marap2024_prod
Source and data from calculation using the default potential

# Description
This folder contains the source code and raw data from the molecular mechanics calculations

# Organization
 - README.md -> current file
 - 01_box_relax -> Relaxation of the initial configuration
 - 02_elastic -> Calculation of the in-plane elastic properties w/ finite differences
 - 03_nanotube -> Simulation of hBN nanotubes
 - 04_torus -> Simulation of hBN nanotori
 - i.basis -> Basis
 - i.basis_opt -> Basis (optimized)
 - i.basis_transpose -> Transposed basis
 - i.basis_transpose_opt -> Transposed basis (optimized)
 - i.parameter.json -> Json file with parameter files
 - i.potential -> Potential file
 - o.box_relax.json -> Raw data from optimized cell
 - o.elastic_compliance.json -> Raw data of compliance matrix
 - o.elastic_stiffness.json -> Raw data of stiffness matrix
 - o.nanotube.csv -> Raw data of hBN nanotubes
 - o.nanotube_proc.csv -> Postprocessed data of hBN nanotubes (csv)
 - o.nanotube_proc.json -> Postprocessed data of fhBN nanotubes (json)
 - o.torus.csv -> Raw data of hBN nanotori
 - o.torus_proc.csv -> Postprocessed data of hBN nanotori (csv)
 - o.torus_proc.json -> Postprocessed data of hBN nanotori (json)
 - pymaster.py -> Copy of the pymaster script
