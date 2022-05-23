#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from utils import iterator
from .pyrwr import PyRWR


class PageRank(PyRWR):
    def __init__(self):
        super().__init__()

    def compute(self,
                c=0.15,
                epsilon=1e-6,
                max_iters=100,
                handles_deadend=True,
                device='cpu'):
        '''
        Compute the PageRank score vector (global ranking)

        inputs
            c : float
                restart probability
            epsilon : float
                error tolerance for power iteration
            max_iters : int
                maximum number of iterations for power iteration
            handles_deadend : bool
                if true, it will handle the deadend issue in power iteration
                otherwise, it won't, i.e., no guarantee for sum of RWR scores
                to be 1 in directed graphs
        outputs
            r : ndarray
                PageRank score vector
        '''

        self.normalize()

        #  q = np.ones((self.n, 1))
        q = np.ones(self.n)
        q = q / self.n

        r, residuals = iterator.iterate(self.nAT, q, c, epsilon,
                                        max_iters, handles_deadend, norm_type=1, device=device)

        return r
