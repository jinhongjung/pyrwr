import numpy as np
from scipy.sparse import csr_matrix

def read_graph(path):
    '''
    Read the graph from the path

    inputs
        path : str
            path for the graph
    outputs
        A : csr_matrix
            sparse adjacency matrix
        base : int
            base of node ids of the graph
    '''
    X = np.loadtxt(path, dtype=float, comments='%')
    m, n = X.shape

    if n == 2:
        # the graph is unweighted
        X = np.c_[ X, np.ones(m) ]
    elif n <= 1 or n >= 4:
        # undefined type, invoerror
        raise FormatError('Invalid input format')

    base = np.amin(X[:, 0:2])
    min_weight = np.amin(X[:, 2])

    if base < 0:
        raise ValueError('Out of range of node ids: negative base')
    if min_weight < 0:
        raise ValueError('Negative edge weights')

    X[:, 0:2] = X[:, 0:2] - base

    row  = X[:, 0]
    col  = X[:, 1]
    data = X[:, 2]

    n = int(np.amax(X[:, 0:2]) + 1) # assume id starts from 0

    A = csr_matrix((data, (row, col)), shape=(n, n))

    return A, base.astype(int)
