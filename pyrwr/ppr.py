import numpy as np
from utils import iterator
from .pyrwr import PyRWR

class PPR(PyRWR):
    def __init__(self):
        pass

    def compute(self, seeds, c=0.15, epsilon=1e-6, max_iters=100,
            handles_deadend=True):

        '''
        Compute the PPR score vector w.r.t. the seed node

        inputs
            seeds : list
                list of seeds
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
                PPR score vector
        '''

        self.normalize()
        seeds = [seed - self.base for seed in seeds]
        if len(seeds) is 0:
            raise ValueError('Seeds are empty')
        if min(seeds) < 0 or max(seeds) >= self.n:
            raise ValueError('Out of range of seed node id')

        q = np.zeros((self.n, 1))
        q[seeds] = 1.0/len(seeds)

        r, residuals = iterator.iterate(self.nAT, q, c, epsilon,
                max_iters, handles_deadend)

        return r
