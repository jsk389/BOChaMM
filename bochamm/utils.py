import numpy as np

from astropy.timeseries import LombScargle
from sloscillations import mixed_modes_utils

#' It is a__file__med that DeltaNu is in μHz
def DeltaPi1_from_DeltaNu_RGB(DeltaNu):
    # Compute Period spacing (in s) from deltanu
    return 60 + 1.7*DeltaNu

def Lor_model(pds, peak):
    return peak.height / (1 + ((pds.frequency.values - peak.frequency)/peak.linewidth)**2)

def sinc2_model(pds, peak):
    deltanu = np.mean(np.diff(pds.frequency.values))
    return peak.height * np.sinc((pds.frequency.values - peak.frequency)/deltanu)**2

def fit_model(pds, peaks):

    model = np.ones_like(pds.frequency.values)

    for i in range(len(peaks)):
        if np.isfinite(peaks.linewidth.iloc[i]):
            model += Lor_model(pds, peaks.iloc[i,])
        else:
            model += sinc2_model(pds, peaks.iloc[i, ])
    return model

def compute_PS_PS(freq, power,  DPi1, q, freqs, lower_tau_lim=1, upper_tau_lim=400):
    # Initial PSxPS to assess starting point and range for Bayesian Optimisation
    params = {'calc_l0': True, # Compute radial mode properties
                'calc_l2': True, # Compute l=2 mode properties
                'calc_l3': False, # Don't need to calculate l=3 theoretical freqs
                'calc_nom_l1': True, # Compute nominal l=1 p-mode properties
                'calc_mixed': False, # Don't compute mixed modes (as not needed)
                'calc_rot': False, # Don't compute rotation
                'DPi1': DPi1,
                'coupling': q,
                'eps_g': 0.0, # Epsilon_g isn't needed for computation of tau due to chosen formulation of zeta
                'l': 1, # Mixed modes are dipole mixed modes
                }
    # Make computation - in our case this is for the computation of zeta
    freqs(params)
    #print(freqs.l0_freqs)
    if freq.min() < freqs.l0_freqs.min():
        power = power[freq >= freqs.l0_freqs.min()]
        zeta = freqs.zeta[freq >= freqs.l0_freqs.min()]
        freq = freq[freq >= freqs.l0_freqs.min()]
    else:
        zeta = freqs.zeta
    #print("PROBLEM IN ZETA COMPUTATION IF ZETA GOES BELOW N=1?!")
    # Compute tau from the zeta value just computed
    new_frequency, tau, zeta = mixed_modes_utils.stretched_pds(freq, 
                                                               zeta)

    # If the search range isn't given then default to frequency range 
    # corresponding to period range of 20-400s
    #if search_range is None:
    f = np.arange(1/(upper_tau_lim), 1/(lower_tau_lim), 0.1/tau.max())
    # import matplotlib.pyplot as plt
    # plt.plot(freq, freqs.zeta)
    # plt.show()
    #else:
    #    f = np.arange(1/search_range[1], 1/search_range[0], 0.1/tau.max())

    # Set up Lomb-Scargle periodogram calculation
    ls = LombScargle(tau, power)
    PSD_LS = ls.power(f)  
    return f, PSD_LS