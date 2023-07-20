from scipy.stats import kstest
import numpy as np 

def perform_kolmogorov_smirnov_test(target_values:np.array, 
                                    reference_values:np.array) -> float:


    return kstest(target_values, reference_values)[1]