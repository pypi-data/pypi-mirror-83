import numpy as np
from scipy.stats import norm

def geokernel( d , h , kernel ):
    
    """  This function corresponds to the kernel functions
        
         d is the distance function between a pair of latitudes 
         h is the half-bandwidth
         kernel corresponds to a specific kernel function  """
    
    
    u = d / h
    
    if kernel == 'uniform':
        kern = ( 1 / 2 ) * ( abs( u ) <= 1 )
    
    elif kernel == 'triangular':
        kern = ( 1 - abs( u ) ) * ( abs( u ) <= 1 )
        
    elif kernel == 'epanechnikov':
        kern = ( 3/4 ) * ( 1 - u ** 2 ) * ( abs( u ) <= 1 )
    
    elif kernel == 'quadratic':
        kern = ( ( 15 / 16 ) * ( 1 - u ** 2 ) ** 2 ) * ( abs( u ) <= 1 )
    
    elif kernel == 'gaussian':
        kern = norm.pdf( u )
    
    
    return( kern )


def PLM( W , Y , L , h , kernel = 'gaussian'):
    
    """  This function corresponds to the Partially Linear Model regression
         
         W is the treatment
         Y is the outcome 
         L is the Latitude 
         h is the half-bandwidth
         kernel corresponds to a specific kernel function  """
    
     
    #Defining the length of control and treated array
    N0 = np.sum( 1 - W )
    N1 = np.sum( W )
    NT = N1 + N0
    
    #Generating the Omega
    Omega = np.zeros( ( NT, NT ) )
    
    totindex = np.arange( NT ).reshape( NT , 1)

    #Fulfilling the Omegas
    for i in range( 0 , NT , 1 ):
        
        dif =  np.abs( L[ i ] - L[ np.arange( np.size( L ) )!= i ] )
        
        kern = geokernel( dif , h , kernel ).T
        
        Omega[ i , np.delete( totindex , i ) ] = kern
        
        if np.sum( Omega[ i , : ]  ) != 0:
            Omega[ i , : ] = Omega[ i , : ] / np.sum( Omega[ i , : ]  )
    
    #Delta is eY
    Delta = Y - np.dot( Omega , Y )
    
    #Genereting alpha
    
    eW = W - np.dot( Omega , W )

    #Genereting a matrix for filtering Sumrows equal to zero
    filtering = totindex[ Omega.sum( axis = 1 ) == 0 ]
    F = np.delete( np.identity( NT ) , filtering , axis = 0 )
    
    eW_F = np.dot( F , eW )
    
    Delta_F = np.dot( F , Delta )
    
    Alpha_F = np.linalg.solve( np.dot ( np.transpose ( eW_F ) , eW_F ) , np.transpose ( eW_F ) )
    
    ate = np.dot( Alpha_F , Delta_F )


    return [ Omega , Delta_F , Alpha_F , ate ]