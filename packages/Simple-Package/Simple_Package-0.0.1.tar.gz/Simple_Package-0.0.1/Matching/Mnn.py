#Defining the matching function for the nearest neighbors (NN) 

def NN( Y, W , L , N , C = None ):
    """ The matching function. 
    
    It pairs each treated (control) observation to the closest control (treatment) 
    observation according to a specific distance. 
    In cases where a treated observation is paired with two or more equidistant observations,
    we average across them.
    The number of matches depends on N's value.
    
    :param Y: It is the outcome variable.
    :type Y: numpy array
    
    :param W: It is the treatment variable. 
    It takes 1 for treated and 0 for control observations.
    :type W: bool
    
    :param L: It is the location variable.
    :type L: numpy array
    
    :param N: It is the number of matched neighbors.
    :type N: int
    
    :param C: It is the caliper to 
    :type N: int
    
    :returns: A tuple of Omega, Delta, ate , atet , atec.
    :rtype: tuple
    
    """
    
    
    #Defining the length of control and treated array
    N0 = np.sum( 1 - W )
    N1 = np.sum( W )
    NT = int( N1 + N0 )
    
    totindex = np.arange( NT ).reshape( NT , 1)
    
    #Getting the index of each observation
    N1index = np.column_stack(( totindex[ W == 1 ] , np.arange( N1 ) ))
    N0index = np.column_stack(( totindex[ W == 0 ] , np.arange( N0 ) ))
    
    #Differentiating the matching variables for control and treated
    L0 = L[ W == 0 ].reshape( N0 , 1 )
    L1 = L[ W == 1 ].reshape( N1 , 1 )
    
    #For getting the n-neighbhors we need KDTree. This convert variables into trees
    L0_tree = KDTree( L0 )
    L1_tree = KDTree( L1 )
    
    L1_d , L1_i = L0_tree.query( L1 , k = N )
    L0_d , L0_i = L1_tree.query( L0 , k = N )
    
    if N == 1:
        size1 = np.size( L1_i )
        size0 = np.size( L0_i )
        
        L1_i = L1_i.reshape( size1 , N)
        L0_i = L0_i.reshape( size0 , N)
        
    
    for i in range( 0 , N ):
        L0_i[ : , i ] = N1index[ L0_i[ : , i ] , 0 ]
        L1_i[ : , i ] = N0index[ L1_i[ : , i ] , 0 ]

    Id = np.concatenate( ( L0_i , L1_i ) )
    
    #Creating the Omega matrix
    Omega = np.zeros( ( NT , NT ) )
    
    if C is None:
        for i in range( 0 , NT ):
            Omega[ i , Id[ i ] ] = ( 1 / N )
    
    else:
        
        trim1 = L1_d <= C
        trim0 = L0_d <= C    
        trim = np.concatenate( ( trim0 , trim1 ) )
        
        for i in range( 0 , NT ):
            k = np.sum( trim[ i ] )
            if k > 0 :
                Omega[ i , Id[ i ] ] = ( 1 / k )* trim[ i ]
    
    #Generating Y_Omega and Delta
    Y_Omega = Omega.dot( Y )
    Delta = Y - Y_Omega
    
    #This vector has the row sum of the Omega matrix
    RowOmega = np.sum( Omega , 1 )
    
    #This chunk of code generate the needed alpha  for calculating ATE, ATEC, ATET
    Alpha_ate = RowOmega[ : , None ] * ( W == 1 ) / sum( RowOmega ) - RowOmega[ : , None ] * ( W == 0 ) / sum( RowOmega )
    Alpha_atet = RowOmega[ : , None ] * ( W == 1 ) / sum( RowOmega[ : , None ] * ( W == 1 ) )
    Alpha_atec =  -1 * ( RowOmega[ : , None ] * ( W == 0 ) / sum( RowOmega[ : , None ] * ( W == 0 ) ) )
    
    #Calculating the ATE, ATET, ATEC
    ate = np.sum( Alpha_ate * Delta )
    atet = np.sum( Alpha_atet * Delta )
    atec = np.sum( Alpha_atec * Delta )
    
    
    return ( Omega, Delta , ate , atet , atec ) 

    