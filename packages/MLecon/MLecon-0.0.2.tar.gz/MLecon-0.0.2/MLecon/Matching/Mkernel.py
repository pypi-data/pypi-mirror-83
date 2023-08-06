from scipy.spatial import KDTree
import numpy as np

def Mkernel( W , Y , L , h , kernel ):
    
    """  This function corresponds to the kernel matching approach
         
         W is the treatment
         Y is the outcome 
         L is the Latitude 
         h is the half-bandwidth
         kernel corresponds to a specific kernel function  """
    
    
    #Defining the length of control and treated array
    N0 = np.sum( 1 - W )
    N1 = np.sum( W )
    NT = N1 + N0
    
    totindex = np.arange( NT ).reshape( NT , 1 )
    
    #Getting the index of each observation
    N1index = np.column_stack(( totindex[ W == 1 ] , np.arange( N1 ) ))
    N0index = np.column_stack(( totindex[ W == 0 ] , np.arange( N0 ) ))
    
    #Differentiating the matching variables for control and treated
    L0 = L[ W == 0 ].reshape( N0 , 1 )
    L1 = L[ W == 1 ].reshape( N1 , 1 )
     
    #Generating the Omega
    Omega = np.zeros( ( NT, NT ) )

    #Fulfilling the Omegas
    for i in range( 0 , N0 , 1 ):
        dif =  np.abs( L0[ i ] - L1 )
        kern = geokernel( dif , h , kernel ).T
        Omega[ N0index[ i , 0 ] , N1index[ : , 0 ] ] = kern

    for i in range( 0 , N1 , 1 ):
        dif =  np.abs( L1[ i ] - L0 )
        kern = geokernel( dif , h , kernel ).T
        Omega[ N1index[ i , 0 ] , N0index[ : , 0 ] ] = kern
    
    for i in range( 0 , NT , 1 ):
        if np.sum( Omega[ i , : ]  ) != 0:
            Omega[ i , : ] = Omega[ i , : ] / np.sum( Omega[ i , : ]  )
        
    #Generating Y_Omega and Delta
    Y_Omega = Omega.dot( Y )
    Delta = Y - Y_Omega
        
    #This vector has the row sum of the matrix Omega
    RowOmega = np.sum( Omega , 1 )
        
    #This chunk of code generate the needed alpha  for calculating ATE, ATEC, ATET
    Alpha_ate = RowOmega[ : , None ] * ( W == 1 ) / sum( RowOmega ) - RowOmega[ : , None ] * ( W == 0 ) / sum( RowOmega )
    Alpha_atet = RowOmega[ : , None ] * ( W == 1 ) / sum( RowOmega[ : , None ] * ( W == 1 ) )
    Alpha_atec =  -1 * ( RowOmega[ : , None ] * ( W == 0 ) / sum( RowOmega[ : , None ] * ( W == 0 ) ) )
    
    #Calculating the ATE, ATET, ATEC
    ate = np.sum( Alpha_ate * Delta )
    atet = np.sum( Alpha_atet * Delta )
    atec = np.sum( Alpha_atec * Delta )
  
    return ( Omega, Delta , ate , atet , atec, Alpha_ate, Alpha_atet , Alpha_atec )