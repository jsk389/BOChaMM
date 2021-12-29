import numpy as np
import time as timer

from . import losses
from turbo import Turbo1, TurboM

class PSxPSOptimisation:
    """
    Class that contains all the computations for optimising the power spectrum of 
    the stretched power spectrum as a function fo the asymptotic l=1 period spacing
    and the coupling factor.
    
    """
    def __init__(self, pds, freqs):
        self.pds = pds
        self.freqs = freqs


    def run_optimisation(self, init_dpi, max_evals=1000, lower_tau_lim=20, upper_tau_lim=400, harmonic=False, use_TurboM=True, verbose=True):
        #, turbo_kwargs=None):
        # TODO: Allow turbo kwargs to be set from function
        # Extract kwargs
        # if turbo_kwargs is None:
        #     turbo_kwargs = dict()
        # else:


        n_init = 100

        f = losses.PSXPS(self.pds, self.freqs, init_dpi=init_dpi, lower_tau_lim=20, upper_tau_lim=400, harmonic=harmonic)

        if use_TurboM:
            turbo_fn = TurboM
        else:
            turbo_fn = Turbo1

        turbo1 = turbo_fn(
            f = f,  # Handle to objective function
            lb = f.lb,  # Numpy array specifying lower bounds
            ub = f.ub,  # Numpy array specifying upper bounds
            n_init = 100,  # Number of initial bounds from an Latin hypercube design
            max_evals = max_evals,  # Maximum number of evaluations
            batch_size = 25,  # How large batch size TuRBO uses
            verbose = verbose,  # Print information from each batch
            use_ard = True,  # Set to true if you want to use ARD for the GP kernel
            max_cholesky_size = 2000,  # When we switch from Cholesky to Lanczos
            n_training_steps = 50,  # Number of steps of ADAM to learn the hypers
            min_cuda = 64,  # Run on the CPU for small datasets
            device = "cpu",  # "cpu" or "cuda"
            dtype = "float64",
            n_trust_regions=4)  # float64 or float32)
        
        
        init_time = timer.time()
        turbo1.optimize()
        #print('Elapsed Time: ', timer.time()-init_time)

        X = turbo1.X  # Evaluated points
        fX = turbo1.fX  # Observed values
        # X.shape, fX.shape
        ind_best = np.argmin(fX)
        f_best, x_best = fX[ind_best], X[ind_best, :]

        #print("Best value found:\n\tf(x) = %.3f\nObserved at:\n\tx = %s" % (f_best, np.around(x_best, 3)))
        return X, fX, turbo1