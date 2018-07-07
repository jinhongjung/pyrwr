import numpy as np
from utils import normalizer, iterator

class RWR:
    def __init__(self, A):
        self.A = A # adjacency matrix
        self.normalized = False
        self.m, self.n = A.shape

    def normalize(self):
        if self.normalized == False:
            nA = normalizer.row_normalize(self.A)
            self.nAT = nA.T
            self.normalized = True

    def compute(self, seed, c=0.15, epsilon=1e-6, max_iters=100):
        self.normalize()

        q = np.zeros((self.n, 1))
        # TODO: check the range of seed
        q[seed] = 1.0

        r, residuals = iterator.iterate(self.nAT, q, c, epsilon,
                max_iters)

        return r
