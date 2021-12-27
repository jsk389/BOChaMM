import numpy as np
import pandas as pd

from astropy.timeseries import LombScargle
from sloscillations import frequencies, mixed_modes_utils

from typing import List, Optional


class PSXPS:
    def __init__(self, pds_l023_removed: pd.DataFrame, 
                 freqs: frequencies.Frequencies, init_dpi: float, 
                 lower_tau_lim: float=20.0, upper_tau_lim: float=400.0, 
                 harmonic: bool=False, 
                 lb: Optional[List[float]]=None,
                 ub: Optional[List[float]]=None) -> None:

        self.freqs = freqs
        self.pds_l023_removed = pds_l023_removed
        if lb is None:
            self.lb = np.array([0.8*init_dpi, 0])
        else:
            self.lb = lb
        if ub is None:
            self.ub = np.array([1.2*init_dpi, 0.8])
        else:
            self.ub = ub
        self.lower_tau_lim = lower_tau_lim
        self.upper_tau_lim = upper_tau_lim
        self.harmonic = harmonic
        
        
    def __call__(self, x):
        assert len(x) == 2
        assert x.ndim == 1
        assert np.all(x <= self.ub) and np.all(x >= self.lb)
        
        DPi1, q = x[0], x[1]
        
        params = {'calc_l0': True, 
                'calc_l2': True, 
                'calc_l3': False, 
                'calc_nom_l1': True,
                'calc_mixed': False, 
                'calc_rot': False,
                'DPi1': DPi1,
                'coupling': q,
                'eps_g': 0.0,
                'l': 1,
                }
        self.freqs(params)
        new_frequency, tau, zeta = mixed_modes_utils.stretched_pds(self.pds_l023_removed.frequency.values, 
                                                                   self.freqs.zeta)

        f = np.arange(1/(self.upper_tau_lim), 1/(self.lower_tau_lim), 0.1/tau.max())
        ls = LombScargle(tau, self.pds_l023_removed.power.values)
        PSD_LS = ls.power(f)
        #noise = np.median(PSD_LS) / (1 - 1/9)**3
        cut_PSD_LS = PSD_LS[(1/f > self.lower_tau_lim) & (1/f < self.upper_tau_lim)]
        cut_f = f[(1/f > self.lower_tau_lim) & (1/f < self.upper_tau_lim)]

        if self.harmonic:
            return -(PSD_LS)[np.argmin(np.abs((1/f) - DPi1/2))] * 1e3
        else:
            return -(PSD_LS)[np.argmin(np.abs((1/f) - DPi1))] * 1e3