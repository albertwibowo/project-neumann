from scipy.stats import chisquare
import numpy as np 

def perform_chi_square(f_obs: np.array, 
                       f_exp: np.array) -> float:
    '''
    MUST ensure f_obs and f_exp have the SAME order. This means
    the values must be sorted this function is called.
    '''

    return chisquare(f_obs=f_obs, f_exp=f_exp)[1]