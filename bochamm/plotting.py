import matplotlib.pyplot as plt
import numpy as np

from sloscillations import frequencies, mixed_modes_utils
from typing import Optional

def plot_stretched_echelle(model_freqs: np.ndarray, model_tau: np.ndarray, 
                           real_freqs: np.ndarray, real_tau: np.ndarray, 
                           DPi1: float, shift: float, heights: Optional[np.ndarray]=None):
    """
    Utility function to plot the stretched echelle for a given set of real and theoretical frequencies
    
    Parameters
    ----------
    model_freqs: np.ndarray
        Theoretical mixed mode frequencies.
        
    model_tau: np.ndarray
        Theoretical mixed mode tau values.
        
    real_freqs: np.ndarray
        Detected peak frequencies.
        
    real_tau: np.ndarray
        Tau values of detected peaks.
        
    DPi1: float
        Period spacing by whcih to compute the stretched echelle.
        
    shift: float
        The computed shift to ensure that the stretched echelle is properly aligned.
        
    heights: Optional[np.ndarray] = None
        Heights of detected peaks. Optional and if given are used to set the size of the 
        markers of the real frequencies in the stretched echelle.
    """
    
    y_real = (real_tau - DPi1*(1/2 + shift))  % DPi1 - DPi1/2
    # The shift is already accounted for in the calculation of the theoretical frequencies, so don't add it in here
    y_theo = (model_tau[:,0] - DPi1/2) % DPi1  - DPi1/2
    y_theo_p1 = (model_tau[:,1] - DPi1/2) % DPi1  - DPi1/2
    y_theo_n1 = (model_tau[:,2] - DPi1/2) % DPi1  - DPi1/2

    if heights is None:
        plt.scatter(y_real, real_freqs)
    else:
        plt.scatter(y_real, real_freqs, s=heights)
    plt.scatter(y_theo, model_freqs[:,0], marker='x')
    plt.scatter(y_theo_p1, model_freqs[:,1], marker='x')
    plt.scatter(y_theo_n1, model_freqs[:,2], marker='x')

def plot_results(pds, summary, l1_peaks, radial_order_range, dpi, coupling, eps_g, split, d01=None, use_heights=True):
    
    freqs = frequencies.Frequencies(frequency=pds.frequency.values,
                                numax=summary.numax.values, 
                                delta_nu=summary.DeltaNu.values if np.isfinite(summary.DeltaNu.values) else None, 
                                epsilon_p=summary.eps_p.values if np.isfinite(summary.eps_p.values) else None,
                                alpha=summary.alpha.values if np.isfinite(summary.alpha.values) else None,
                                radial_order_range=radial_order_range)
    params = {'calc_l0': True, # Compute radial mode properties
            'calc_l2': True, # Compute l=2 mode properties
            'calc_l3': False, # Don't need to calculate l=3 theoretical freqs
            'calc_nom_l1': True, # Compute nominal l=1 p-mode properties
            'calc_mixed': True, # Don't compute mixed modes (as not needed)
            'calc_rot': True, # Don't compute rotation
            'DPi1': dpi,
            'coupling': coupling,
            'eps_g': eps_g,
            'split_core': split,
            'split_env': 0.0,
            'l': 1, # Mixed modes are dipole mixed modes
            }
    if d01 is not None:
        params["d01"] = d01

    # Make computation - in our case this is for the computation of zeta
    freqs(params)

    #print(freqs.DPi1)
    freqs.generate_tau_values()

    new_peaks_tau = mixed_modes_utils.peaks_stretched_period(l1_peaks.frequency.values, 
                                                                pds.frequency.values, 
                                                                freqs.tau)
    new_peaks_zeta = mixed_modes_utils.peaks_stretched_period(l1_peaks.frequency.values, 
                                                                pds.frequency.values, 
                                                                freqs.zeta)
    new_peaks_tau -= freqs.shift*freqs.DPi1
    plt.figure(figsize=(12,8))
    plot_stretched_echelle(np.c_[freqs.l1_mixed_freqs, freqs.l1_mixed_freqs_p1, freqs.l1_mixed_freqs_n1], 
                           np.c_[freqs.l1_mixed_tau, freqs.l1_mixed_tau_p1, freqs.l1_mixed_tau_n1], 
                           l1_peaks.frequency.values, new_peaks_tau, freqs.DPi1, shift=0.0, heights=l1_peaks.height*5)
    # Don't include shift in plot of echelle as shift already included
    for i in freqs.l1_nom_freqs:
        plt.axhline(i, color='k', linestyle='--', alpha=0.5)
    plt.xlabel(r'$\tau\;\mathrm{mod}\;\Delta\Pi_{1}$ (s)', fontsize=18);
    plt.ylabel(r'Frequency ($\mu$Hz)', fontsize=18);
    
    return freqs, new_peaks_tau
