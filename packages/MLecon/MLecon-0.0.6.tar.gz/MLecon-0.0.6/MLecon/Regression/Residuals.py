# Separate residual function
import numpy as np
    
def residuals( Y , X ) :

    "This function estimates the residuals of the regression of Y on X"

    # e = Y - X * (X' * X ) ^ (-1) * X' * Y\n",
    # e = Y - X * solve[ (L'*L) , L' ]  * Y\n",
    # e = Y -          Z                * Y\n",

    Z = np.dot ( X , np.linalg.solve( np.dot ( np.transpose( X ) , X ) , np.transpose( X ) ) )

    e = Y - np.dot( Z ,  Y )

    return e