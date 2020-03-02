#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.sparse import spdiags


def row_normalize(A):
    '''
    Perform row-normalization of the given matrix

    inputs
        A : crs_matrix
            (n x n) input matrix where n is # of nodes
    outputs
        nA : crs_matrix
             (n x n) row-normalized matrix
    '''
    n = A.shape[0]

    # do row-wise sum where d is out-degree for each node
    d = A.sum(axis=1)
    d = np.asarray(d).flatten()

    # handle 0 entries in d
    d = np.maximum(d, np.ones(n))
    invd = 1.0 / d

    invD = spdiags(invd, 0, n, n)

    # compute row normalized adjacency matrix by nA = invD * A
    nA = invD.dot(A)

    return nA
