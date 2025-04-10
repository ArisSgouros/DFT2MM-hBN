import numpy as np
from scipy.optimize import minimize
import csv
import sys

k2Pi_3 = np.pi*2.0/3.0

# specify the number of cells along a and z directions
n_cell_a = 1
n_cell_z = 1
#phi_max  = np.radians(10.0)
phi_max  = 0.53
constraint_positive_coeff = False
#
# read the total deformation energy and convert it to the cell level
#
phi_list = []
Ed_a_list = []
Ed_z1_list = []
Ed_z2_list = []
Et_a_list = []
Et_z1_list = []
Et_z2_list = []
with open('torsion_energy.csv', 'r') as file:
    reader = csv.reader(file)
    # skip header
    next(reader)
    for row in reader:
        [phi, Ed_a, Ed_z1, Ed_z2] = row
        if float(phi) > phi_max: continue

        phi_list.append(float(row[0]))
        Ed_a_list.append(float(row[1]) / n_cell_a)
        Ed_z1_list.append(float(row[2]) / n_cell_z)
        Ed_z2_list.append(float(row[3]) / n_cell_z)
n_phi = len(phi_list)
#
# remove the contribution due to bending
#
# define the conversions phi->theta
def the_a(x):
    return 2.0 * np.arcsin(np.sqrt(3.0/8.0) * np.sqrt(np.cos(x) + 1.0))
def the_z(x):
    return 2.0 * np.arcsin(1.0/2.0 * np.sqrt(2.0 + np.cos(x)))
# define the bending potential
def V_b(x):
    #return ( 8.059575*(x - k2Pi_3)**2 - 2.677*(x - k2Pi_3)**3 )
    return ( 2.685*(x - k2Pi_3)**2 - 1.78*(x - k2Pi_3)**3 ) # k/2 k'/3
#Removing the E_bend contribution#\n",
for ii in range(n_phi):
    phi = phi_list[ii]
    Ed_a = Ed_a_list[ii]
    Et_a = Ed_a - 2*V_b(the_a(phi))
    Et_a_list.append(Et_a)
    Ed_z1 = Ed_z1_list[ii]
    Et_z1 = Ed_z1 - 2*V_b(the_z(phi))
    Et_z1_list.append(Et_z1)
    Ed_z2 = Ed_z2_list[ii]
    Et_z2 = Ed_z2 - 2*V_b(the_z(phi))
    Et_z2_list.append(Et_z2)
# export the total and pure torsion contributions
#for ii in range(n_phi):
#    print(ii, phi_list[ii], Ed_a_list[ii], Ed_z1_list[ii], Et_a_list[ii], Et_z1_list[ii])
#
# define the phi-ww conversions
def w_1a(x):
    return ( np.arccos(-np.cos(x)) )
def w_2a(x):
    return ( np.arccos(np.sqrt(3)*(1+np.cos(x))/np.sqrt(9*np.sin(x)**2+6*(1+np.cos(x)))) )
def w_3a(x):
    return ( np.arccos(-np.sqrt(3)*(1+np.cos(x))/np.sqrt(9*np.sin(x)**2+6*(1+np.cos(x)))) )
def w_1z(x):
    return ( np.arccos(np.sqrt(3/(np.sin(x)**2+3))) )
def w_2z(x):
    return ( np.arccos(-np.sqrt(3/(np.sin(x)**2+3))) )
def w_3z(x):
    return ( np.arccos(np.sqrt(3/(np.sin(x)**2+3))*np.cos(x)))
def w_4z(x):
    return ( np.arccos(-np.sqrt(3/(np.sin(x)**2+3))*np.cos(x)))
#
# Model 1
# torsional potential
#def V_t(cc, x):
#    return 0.5*cc[0]*(1.0 + np.cos(x)) + 0.5*cc[1]*(1.0 - np.cos(2.0*x))
# total torsional potential for deformation along the a or z direction
#def U_ta(cc, x):
#    return ( 2.0 * V_t(cc,w_1a(x)) + 4.0 * V_t(cc,w_2a(x)) + 4.0 * V_t(cc,w_3a(x)) )
#def U_tz(cc, x):
#    return ( 2.0 * V_t(cc,w_1z(x)) + 2.0 * V_t(cc,w_2z(x)) + 2.0 * V_t(cc,w_3z(x)) + 2.0 * V_t(cc,w_4z(x)) )
#
# Model 2
#
# torsional potential of cis and trans torsion angles
def V_t(kk, x):
    return kk * ( 1.0 - np.cos(2.0*x))
## total torsional potential for deformation along the a or z direction

def U_ta(cc, x):
    [kcis, ktrans] = cc
    return ( 2.0 * V_t(ktrans,w_1a(x)) + 4.0 * V_t(kcis,w_2a(x)) + 4.0 * V_t(ktrans,w_3a(x)) )
def U_tz(cc, x):
    [kcis, ktrans] = cc
    return ( 2.0 * V_t(kcis,w_1z(x)) + 2.0 * V_t(ktrans,w_2z(x)) + 2.0 * V_t(kcis,w_3z(x)) + 2.0 * V_t(ktrans,w_4z(x)) )

# define the objective function to be minimized
def ObjFun(xx_list):
    merit = 0.0

    # apply constraints
    if constraint_positive_coeff:
       for ixx in xx_list:
          if ixx < 0:
             return 1000000

    weight = 0.0
    for ii in range(n_phi):
        phi = phi_list[ii]

        # a direction
        idata = Et_a_list[ii]
        imodel = U_ta(xx_list, phi)
        merit += (idata - imodel)**2
        weight += 1.0

        # z1 direction
        idata = Et_z1_list[ii]
        imodel = U_tz(xx_list, phi)
        merit += (idata - imodel)**2
        weight += 0.5

        # z2 direction
        idata = Et_z2_list[ii]
        imodel = U_tz(xx_list, phi)
        merit += (idata - imodel)**2
        weight += 0.5

    merit /= weight
    #print("    residual, coeffs: ", merit, xx_list)

    return merit

# set initial guess
coeff_list = np.array([0.1, 0.1])

res = minimize(ObjFun, coeff_list, method='nelder-mead',options={'xtol': 1e-7, 'disp': True})
coeff_list = res.x
if res.success:
   print("Coeffs: ", coeff_list)
   print("Residual: ", ObjFun(coeff_list))

# plot
print("plot\n")
print("phi dft_Ed_ac dft_Et_ac model_Eb_ac model_Et_ca dft_Ed_zz1 dft_Et_zz1 model_Eb_zz1 model_Et_zz1 dft_Ed_zz2 dft_Et_zz2 model_Eb_zz2 model_Et_zz2")
for ii in range(n_phi):
   phi = phi_list[ii]

   Eb_ac = 2*V_b(the_a(phi))
   Eb_z1 = 2*V_b(the_z(phi))
   Eb_z2 = 2*V_b(the_z(phi))

   print(phi, Ed_a_list[ii], Et_a_list[ii], Eb_ac, U_ta(coeff_list, phi), Ed_z1_list[ii], Et_z1_list[ii], Eb_z1, U_tz(coeff_list, phi), Ed_z2_list[ii], Et_z2_list[ii], Eb_z2, U_tz(coeff_list, phi))
