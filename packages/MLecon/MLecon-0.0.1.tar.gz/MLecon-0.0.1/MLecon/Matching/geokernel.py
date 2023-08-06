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