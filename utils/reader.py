#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.sparse import csr_matrix, find


def read_directed_graph(X, weighted):
    rows = X[:, 0]
    cols = X[:, 1]
    data = X[:, 2]

    # assume id starts from 0
    n = int(np.amax(X[:, 0:2])) + 1

    # the weights of redundant edges will be summed (by default in csr_matrix)
    A = csr_matrix((data, (rows, cols)), shape=(n, n))

    if not weighted:
        # no redundant edges are allowed for unweighted graphs
        I, J, K = find(A)
        A = csr_matrix((np.ones(len(K)), (I, J)), shape=A.shape)

    return A


def read_undirected_graph(X, weighted):
    rows = X[:, 0]
    cols = X[:, 1]
    data = X[:, 2]

    # assume id starts from 0
    n = int(np.amax(X[:, 0:2])) + 1

    # the weights of redundant edges will be summed (by default in csr_matrix)
    _A = csr_matrix((data, (rows, cols)), shape=(n, n))

    # this is under the assumption that src_id <= dst_id for all edges (see line 80 in this code)
    A = _A + _A.T

    if not weighted:
        # no redundant edges are allowed for unweighted graphs
        I, J, K = find(A)
        A = csr_matrix((np.ones(len(K)), (I, J)), shape=A.shape)

    return A


def swap_columns(X):
    # make src_id <= dst_id
    b_idx = X[:, 0] > X[:, 1]
    a_idx = np.logical_not(b_idx)

    B = X[b_idx, :]
    B[:, [0, 1]] = B[:, [1, 0]] # swap columns

    A = X[a_idx, :]

    return np.vstack((A, B))


def read_graph(path, graph_type):
    '''
    Read the graph from the path

    inputs
        path : str
            path for the graph
        graph_type : str
            type of graph {'directed', 'undirected', 'bipartite'}
    outputs
        A : csr_matrix
            sparse adjacency matrix
        base : int
            base of node ids of the graph
    '''
    X = np.loadtxt(path, dtype=float, comments='#')
    m, n = X.shape

    weighted = True
    if n == 2:
        # the graph is unweighted
        X = np.c_[ X, np.ones(m) ]
        weighted = False
    elif n <= 1 or n >= 4:
        # undefined type
        raise FormatError('Invalid input format')

    base = np.amin(X[:, 0:2])
    min_weight = np.amin(X[:, 2])

    if base < 0:
        raise ValueError('Out of range of node ids: negative base')
    if min_weight < 0:
        raise ValueError('Negative edge weights')

    # make node id start from 0
    X[:, 0:2] = X[:, 0:2] - base

    if graph_type == "directed":
        A = read_directed_graph(X, weighted)
    elif graph_type == "undirected":
        # make src_id <= dst_id
        X = swap_columns(X)
        A = read_undirected_graph(X, weighted)
    elif graph_type == "bipartite":
        pass
    #    A = _read_bipartite_graph(X)
    else:
        raise ValueError('graph_type sould be directed, undirected, or bipartite')

    return A, base.astype(int)
