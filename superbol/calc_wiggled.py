#calc_wiggled.py

import numpy as np
from superbol import flux_wiggler
from superbol import fqbol

num_wiggled_seds = 10

#Parallel via MPI
def wiggle_fluxes_n_times(sed):
    wiggled_qbol_fluxes = [None] * num_wiggled_seds
    for i in range(num_wiggled_seds):
        #Make a copy of the original sed
        sed_copy = flux_wiggler.copy_flux_list(sed)
        #Wiggle each flux at each time point in sed
        wiggled_sed = flux_wiggler.wiggle_fluxes(sed_copy)
        #Integrate wiggled sed to get wiggled qbol flux
        wiggled_qbol_fluxes[i] = fqbol.SplineIntegralCalculator().calculate(wiggled_sed)
    #print("\nList of wiggled qbol fluxes: ", wiggled_qbol_fluxes) 
    #print("\nType of wiggled_qbol_fluxes: ", type(wiggled_qbol_fluxes))
    #print("\nType of item in wiggled_qbol_fluxes: ", type(wiggled_qbol_fluxes[0]))
    return wiggled_qbol_fluxes

#Once at the end - nonparallel
def calc_avg_stdev(sed):
    #Wiggle the fluxes
    wiggled_qbol_fluxes = wiggle_fluxes_n_times(sed)
    #Calculate avg, stdev
    average_qbol_flux = np.average(wiggled_qbol_fluxes)
    stdev_qbol_flux = np.std(wiggled_qbol_fluxes)
    
    return [average_qbol_flux, stdev_qbol_flux]

