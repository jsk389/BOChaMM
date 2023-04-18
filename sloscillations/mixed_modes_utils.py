# -*- coding: utf-8 -*-

import itertools
import numpy as np 
import matplotlib.pyplot as plt

from scipy import interpolate
from scipy.integrate import quad



def all_mixed_l1_freqs(delta_nu, nu_zero, nu_p, DPi1, eps_g, coupling, return_order=True, method='Mosser2018_update'):

    l1_freqs = []
    l1_g_freqs = []
    order = []
    N_g = []

    if method == "Mosser2018_update":
        search_function = find_mixed_l1_freqs_Mosser2018_update
    else:
        sys.exit("Other methods not yet implemented")

    for i in range(len(nu_p)):

        if nu_p[i] > nu_zero[-1]:
            radial = np.array([nu_zero[-1], nu_zero[-1] + delta_nu[i]])
        else:
            radial = np.array([nu_zero[i], nu_zero[i+1]])
            
        tmp, tmp_g, tmp_ng = search_function(delta_nu[i], radial, nu_p[i], 
                                         DPi1, eps_g, coupling)
        order.append([i]*len(tmp))
        l1_freqs.append(tmp)
        l1_g_freqs.append(tmp_g)
        N_g.append(tmp_ng)

    if return_order:
        return np.array(list(itertools.chain(*l1_freqs))), \
               np.array(list(itertools.chain(*order))), \
               np.array(list(itertools.chain(*l1_g_freqs))), \
               np.array(list(itertools.chain(*N_g)))
    else:
        return np.array(list(itertools.chain(*l1_freqs)))



def find_mixed_l1_freqs_Mosser2018_update(delta_nu, nu_zero, nu_p, DPi1, eps_g, coupling):
    """
    Helper function for our update to Mosser 2018 method (addition of 1/2 in nmin and nmax e.g.)
    """

    nmin = np.floor(1 / (DPi1*1e-6 * nu_zero[1]) - (1/2) - eps_g)
    nmax = np.floor(1 / (DPi1*1e-6 * nu_zero[0]) - (1/2) - eps_g)
    #print('NU ZERO: ', nu_zero)

    N_modes = (delta_nu * 1e-6) / (DPi1 * (nu_p*1e-6)**2)

    N = np.arange(nmin, nmax + 2, 1)

    frequencies, g_mode_freqs, N_g = find_mixed_l1_freq_Mosser2018_update_(delta_nu, nu_zero, nu_p, DPi1, eps_g, coupling, N)

    idx = np.argsort(frequencies[np.isfinite(frequencies)])
    return frequencies[np.isfinite(frequencies)][idx], g_mode_freqs[np.isfinite(frequencies)][idx], N_g[np.isfinite(frequencies)][idx]


def opt_funcM(nu, nu_g, pzero, pone, DPi1, coupling):
    theta_p = (np.pi / (pzero[1]-pzero[0])) * (nu - pone)
    theta_g = np.pi/DPi1 * 1e6 * (1/nu - 1/nu_g) + np.pi/2
    y = np.tan(theta_p) - coupling * np.tan(theta_g)
    return y  


def find_mixed_l1_freq_Mosser2018_update_(delta_nu, pzero, pone, DPi1, eps_g, coupling, N):
    """
    Find mixed modes using updated Mosser 2018 method.
    """

    nu_g = 1 / (DPi1*1e-6 * (N + 1/2 + eps_g))
    # Go +/- 1/2 * DPi1 away from g-mode period
    lower_bound = 1 / (DPi1*1e-6 * (N     + 1/2  + 1/2 + eps_g)) + 0.220446049250313e-16 * 1e4 #np.finfo(float).eps * 1e4
    upper_bound = 1 / (DPi1*1e-6 * (N - 1 + 1/2  + 1/2 + eps_g)) - 0.220446049250313e-16 * 1e4#np.finfo(float).eps * 1e4

    solns = []

    for i in range(len(nu_g)):
        if (upper_bound[i] > pzero[1]):
            upper_bound[i] = pzero[1]
        elif (lower_bound[i] < pzero[0]):
            lower_bound[i] = pzero[0]
        if (upper_bound[i] < lower_bound[i]) or (lower_bound[i] > upper_bound[i]):
            pass
        else:
            ff = np.linspace(lower_bound[i], upper_bound[i], 1000)
            y = opt_funcM(ff, nu_g[i], pzero, pone, DPi1, coupling)           
            idx = np.where(np.diff(np.sign(y)) > 0)[0]
           
            if len(idx) > 0:
                solns = np.append(solns, ff[idx])


    theta_p = (np.pi / (pzero[1]-pzero[0])) * (solns - pone)
    # Approximate pure g-mode frequencies and radial orders
    g_period = 1/(solns*1e-6) - DPi1/np.pi * np.arctan2(np.tan(theta_p), coupling) 

    n_g = np.floor(g_period / DPi1 - eps_g - 1/2)
    return solns, 1e6/g_period, n_g



def _interpolated_zeta(frequency, delta_nu, nu_zero, nu_p, coupling, DPi1, plot=False):
    """
    Compute zeta for each radial order
    """
    zeta_max = np.zeros(len(nu_p))
    model = np.zeros_like(frequency)
    for i in range(len(nu_p)):
        # Only compute θₚ from one radial mode frequency to the next
        if i == len(nu_zero)-1:
            dnu = delta_nu[i] + (delta_nu[i] - delta_nu[i-1])
            cond = (frequency > nu_zero[i]) & (frequency < nu_zero[i] + dnu)
            
            # Estimate deltanu from radial mode frequencies
        else:
            cond = (frequency > nu_zero[i]) & (frequency < nu_zero[i+1])
            dnu = delta_nu[i]
        
        θₚ = np.pi*(frequency[cond] - nu_p[i])/dnu
        N = (dnu*1e-6)/(DPi1 * (nu_p[i]*1e-6)**2)
        frac = 1 + (coupling/N) * (coupling**2*np.cos(θₚ)**2 + np.sin(θₚ)**2)**-1
        zeta_max[i] = 1/(1 + coupling/N)
        if plot:
            plt.plot(frequency[cond], frac**-1 + (1 - zeta_max[i]))
        model[cond] = frac**-1 + (1 - zeta_max[i])
    return model, zeta_max

def interpolated_zeta(frequency, delta_nu, nu_zero, nu_p, coupling, DPi1, plot=False):
    """
    Compute the mixing function zeta for all frequency values

    Inputs:

        :params freq: Full frequency array
        :type   freq: numpy.ndarray

        :params delta_nu: Large frequency separation
        :type   delta_nu: float

        :params nu_zero: Array of radial mode frequencies
        :type   nu_zero: numpy.ndarray

        :params nu_p: Array of nominal p-mode frequencies
        :type   nu_p: numpy.ndarray

        :params coupling: Mode coupling
        :type   coupling: float

        :params DPi1: l=1 period spacing
        :type   DPi1: float

    """
   
   # N = (delta_nu*1e-6)/(DPi1 * (nu_p*1e-6)**2)
    
    #zeta_max = (1 + (coupling/N))**-1
    #zeta_min = (1 + (1/(coupling*N)))**-1

    # Compute zeta over each radial order
    
    model, zeta_max = _interpolated_zeta(frequency, delta_nu, nu_zero, nu_p, 
                         coupling, DPi1, plot=plot)

    backg = np.interp(frequency, nu_p, zeta_max)
    
    # Add background back into zeta
    full_model = model - (1 - backg)
    
    return full_model #, zeta_max, zeta_min


def zeta_interp(freq, nu_zero, nu_p, delta_nu, 
                DPi1, coupling, eps_g,
                numDPi1=100, DPi1_range=[0.99, 1.01], return_full=False):
    # Interpolate zeta function
    l1_freqs = []
    zeta = []
    DPi1_vals = np.linspace(DPi1_range[0]*DPi1, DPi1_range[1]*DPi1, numDPi1)

    for i in range(len(DPi1_vals)):
        #print(DPi1_vals[i])
        tmp_l1_freqs, tmp_zeta = old_all_mixed_l1_freqs(delta_nu, nu_zero, nu_p, DPi1_vals[i], eps_g, coupling, return_order=False, calc_zeta=True)

        l1_freqs = np.append(l1_freqs, tmp_l1_freqs)
        zeta = np.append(zeta, tmp_zeta)
        

    l1_freqs = l1_freqs.ravel()
    zeta = zeta.ravel()

    idx = np.argsort(l1_freqs)
    l1_freqs = l1_freqs[idx]
    zeta = zeta[idx]

    zeta_fun = interpolate.interp1d(l1_freqs, zeta)

    if return_full:
        return l1_freqs, zeta, zeta_fun
    return zeta_fun

def stretched_pds(frequency, zeta, oversample=1):
    # Compute frequency bin-width
    bw = frequency[1]-frequency[0]

    # Compute dtau
    if oversample > 1:
        frequency = np.arange(frequency.min(), frequency.max(), bw/oversample)
        zeta = np.interp(frequency, frequency, zeta)
        dtau = 1 / (zeta*(frequency*1e-6)**2)
    else:
        dtau = 1 / (zeta*(frequency*1e-6)**2)
    

    # Compute tau
    tau = np.cumsum(dtau)*(bw/oversample * 1e-6)# + 13.8
 
    return frequency, tau, zeta #, shift

def compute_tau_shift(tau, DPi1):
    """
    Compute shift in tau to line up m=0 at tau mod DeltaPi1 = 0
    """
    # There is a problem when the value of tau % DPi is on the border of here there is wrapping
    # and so to check for that we compute both the median and the mean, if they vary by more than 5e-2
    # then we automatically set to 0 as an approximation.
    # Compute shift properly
    mean_shift = np.mean(((tau % DPi1) / DPi1) - 1)
    median_shift = np.median(((tau % DPi1) / DPi1) - 1)
    if np.abs(mean_shift - median_shift) < 5e-2:
        return mean_shift
    else:
        return 0.0


def peaks_stretched_period(frequency, pds_frequency, tau):
    assert len(tau) == len(pds_frequency)
    return np.interp(frequency, pds_frequency, tau)


