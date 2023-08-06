def regression_kernel( W , Y , L , h , kernel = 'gaussian'):
    
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