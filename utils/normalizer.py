import numpy as np
from scipy.sparse import spdiags

def row_normalize(A):
    '''
    Perform row-normalization of the given matrix

    inputs
        A : crs_matrix
            input matrix
    outputs
        nA : crs_matrix
            row normalized matrix
    '''
    m, n = A.shape
    # row-wise sum, d is out-degree for each node
    d = A.sum(axis=1)

    # handling 0 entries
    d = np.maximum(d, np.ones((n, 1)))
    invd = 1.0 / d
    invd = np.reshape(invd, (1,-1))
    invD = spdiags(invd, 0, m, n)

    # row normalized adj. mat. 
    nA = invD * A

    return nA

