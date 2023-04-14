import matplotlib.pyplot as plt
import numpy as np

class Thresholding:

    def __init__(self, data: np.ndarray, fX: np.ndarray):
        self.data = data
        self.fX = fX

    def find_threshold(self, plot: bool=False):
        """
        Find appropriate threshold from Bayesian optimisation output.
        """
        acc_fX = np.minimum.accumulate(self.fX)
        neg_max_fX = np.max(-self.fX)
        y = -acc_fX/neg_max_fX

        # Interpolate
        interp_x = np.linspace(0, len(self.fX)-1, 10_000)
        x = np.linspace(0, len(self.fX)-1, len(self.fX))
        interp_y = np.interp(interp_x, x, y)
        interp_fX = np.interp(interp_x, x, self.fX)
        interp_thresh = np.minimum.accumulate(interp_fX)[np.argmin(np.abs(interp_y - 0.5))]

        if plot:

            fig = plt.figure(figsize=(20, 8))
            plt.plot(self.fX, 'b.', ms=10)  # Plot all evaluated points as blue dots
            plt.plot(acc_fX, 'r', lw=3)  # Plot cumulative minimum as a red line
            plt.axhline(acc_fX[np.argmin(np.abs(y - 0.5))], color='r', linestyle='--', lw=3, label=r'Original threshold')
            plt.axhline(interp_thresh, color='g', linestyle='--', label=r'Interpolated threshold')
            plt.legend(loc='best')
            plt.show()

            plt.figure(figsize=(20,8))
            plt.plot(-acc_fX/neg_max_fX)
            plt.axhline(-acc_fX[np.argmin(np.abs(y - 0.5))]/neg_max_fX, color='r', linestyle='--', lw=3, label=r'Original threshold')
            plt.ylabel(r'Normalised accumulated maximum of loss', fontsize=24)
            plt.axhline(-interp_thresh/np.max(-interp_fX), color='g', linestyle='--', label=r'Interpolated threshold')
            plt.legend(loc='best')
            plt.show()

            plt.figure(figsize=(20,8))
            plt.hist(-self.fX, bins=20, density=True);
            plt.axvline(np.percentile(-self.fX, 50.0), color='r', linestyle='--', label=r'Median of loss')
            plt.axvline(-interp_thresh, color='g', linestyle='--', label=r'Median of accumulated loss')
            plt.xlabel(r'Loss', fontsize=24)
            plt.ylabel(r'Probability Density', fontsize=24)
            plt.legend(loc='best')   
            plt.show()

        return -interp_thresh

    def reduce_data(self, threshold: float):
        return self.data[(-self.fX > threshold), :], self.fX[(-self.fX > threshold)]

    def __call__(self, return_threshold: bool=True, plot: bool=False):

        thresh = self.find_threshold(plot=plot)
        reduced_data, reduced_loss = self.reduce_data(thresh)
        if return_threshold:
            return reduced_data, reduced_loss, thresh
        else:
            return reduced_data