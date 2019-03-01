#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    # do row-wise sum where d is out-degree for each node
    d = A.sum(axis=1)
    d = np.asarray(d).flatten()

    # handle 0 entries in d
    d = np.maximum(d, np.ones(n))
    invd = 1.0 / d

    invD = spdiags(invd, 0, m, n)

    # compute row normalized adjacency matrix by nA = invD * A
    nA = invD.dot(A)

    return nA
