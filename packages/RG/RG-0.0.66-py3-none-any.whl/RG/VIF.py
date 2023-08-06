#%% VIF (Variance Inflation Factor)

import numpy as np
import statsmodels.api as sm
import RG as rg

def VIF(X0):

    # Make a bunch of models
    # Each model contains all but 1 variable
    # That variable is predicted using the others
    # This is acheived with the "selector" variable
    n,k = X0.shape
    R2_i = np.zeros((k,1))
    VIF_i = np.zeros((k,1))
    
    for i in range(k):
        selector = [X0 for X0 in range(X0.shape[1]) if X0 != i]
        X = X0[:,selector]
        y = X0[:,i]
    
        X = sm.add_constant(X) ## Add an intercept (beta_0) to our model
        b, b_int, model, R2, F, p = rg.regress(y, X)
        R2_i[i] = R2
        VIF_i[i] = 1/(1-R2)
        
    return VIF_i, R2_i
    
