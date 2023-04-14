import numpy as np

from . import (
    clustering,
    thresholding
)

from collections import namedtuple
from turbo.turbo import turbo_1, turbo_m
from typing import Union

Results = namedtuple('Results', ['extraction_class', 'reduced_data', 'reduced_loss', 'threshold', 'reduced_cluster_labels'])
def extract_results(data: np.ndarray, loss: np.ndarray, bayes_opt_method: Union[turbo_1.Turbo1, turbo_m.TurboM], 
                   extraction_method: Union[clustering.Clustering, thresholding.Thresholding],
                   extraction_kwargs: dict={}):
    """
    Extract results from the Bayesian Optimisation using a given extraction method.
    """
    if extraction_method == "clustering":
        extraction_class = clustering.Clustering(data, loss)
        reduced_data, reduced_loss, cluster_labels = extraction_class(**extraction_kwargs)
        #print("Clustering")
        return Results(extraction_class=extraction_class, reduced_data=reduced_data, 
                       reduced_loss=reduced_loss, threshold=None, reduced_cluster_labels=cluster_labels)

    elif extraction_method == "thresholding":
        extraction_class = thresholding.Thresholding(data, loss)
        reduced_data, reduced_loss, threshold = extraction_class(**extraction_kwargs)
        #print("Thresholding")
        return Results(extraction_class=extraction_class, reduced_data=reduced_data, 
                       reduced_loss=reduced_loss, threshold=threshold, reduced_cluster_labels=None)
    else:
        raise NameError("Supplied extraction method does not exists! Should be instance of either clustering or thresholding.")
