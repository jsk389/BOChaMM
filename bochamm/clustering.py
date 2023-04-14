import matplotlib.pyplot as plt
import numpy as np

from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from typing import Optional

class Clustering:
    """
    Run clustering on points from Bayesian Optimisation
    """

    def __init__(self, data: np.ndarray, loss: np.ndarray):

        self.data = data
        self.loss = loss

    def __call__(self, eps: Optional[float]=None, min_samples: int=30,
                    n_neighbours: int=3, verbose: bool=False, plot: bool=False):

        self.clustering_algorithm = self.cluster(eps=eps, min_samples=min_samples, n_neighbours=n_neighbours, verbose=verbose, plot=plot)

        reduced_data, reduced_loss, labels = self.reduce_data()

        return reduced_data, reduced_loss, labels

    def reduce_data(self):
        """
        Reduce data according to clustering
        """
        
        cond = self.clustering_algorithm.labels_ >= 0
        return self.data[cond, :], self.loss[cond], self.clustering_algorithm.labels_[cond]


    def cluster(self, eps: Optional[float]=None, min_samples: int=30,
                    n_neighbours: int=3, verbose: bool=False, plot: bool=False):
        """
        Cluster the supplied points using the DBSCAN algorithm with the supplied
        epsilon and minimum samples.
        
        """
        if eps is None:
            eps = self.find_best_epsilon(n_neighbours=n_neighbours, verbose=verbose, plot=plot)
        
        m = DBSCAN(eps=eps, min_samples=min_samples)
        m.fit(self.data)    

        return m

    # https://iopscience.iop.org/article/10.1088/1755-1315/31/1/012012/pdf
    def find_best_epsilon(self, n_neighbours: int=3, verbose: bool=False, plot: bool=False) -> float:
        neigh = NearestNeighbors(n_neighbors=3)
        nbrs = neigh.fit(self.data)
        distances, indices = nbrs.kneighbors(self.data)

        distances = np.sort(distances, axis=0)
        distances = distances[:,1]

        XX = np.c_[np.linspace(1, len(distances), len(distances)), distances]
        idxs = self.find_elbow(XX, self.get_data_radiant(XX))   

        eps = XX[idxs, 1]
        #if verbose:
        #    print(f"Chosen epsilon value is {eps}")    
        if plot:
            plt.plot(XX[:,0], XX[:,1])
            plt.axhline(XX[idxs,1], color='g', linestyle='--', label=r'"Optimal" epsilon')
            plt.axhline(XX[idxs,1], color='r', linestyle='--')
            plt.xlabel(r'Sorted Index', fontsize=18)
            plt.ylabel(r'Distance to 3rd nearest neighbour', fontsize=18)
            plt.legend(loc='best')
            plt.show()
        return eps

    #https://datascience.stackexchange.com/questions/57122/in-elbow-curve-how-to-find-the-point-from-where-the-curve-starts-to-rise
    def find_elbow(self, data: np.ndarray, theta: np.ndarray) -> np.ndarray:

        # make rotation matrix
        co = np.cos(theta)
        si = np.sin(theta)
        rotation_matrix = np.array(((co, -si), (si, co)))

        # rotate data vector
        rotated_vector = data.dot(rotation_matrix)

        # return index of elbow
        return np.where(rotated_vector == rotated_vector.min())[0][0]

    def get_data_radiant(self, data: np.ndarray) -> np.ndarray:
        return np.arctan2(data[:, 1].max() - data[:, 1].min(), 
                        data[:, 0].max() - data[:, 0].min())