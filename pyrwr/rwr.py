import numpy as np
from utils import reader, normalizer, iterator

class RWR:
    def __init__(self):
        self.normalized = False
        pass

    def read_graph(self, input_path):
        self.A, self.base = reader.read_graph(input_path)
        self.m, self.n = self.A.shape
        self.normalize()

    def normalize(self):
        if self.normalized == False:
            nA = normalizer.row_normalize(self.A)
            self.nAT = nA.T
            self.normalized = True

    def compute(self, seed, c=0.15, epsilon=1e-6, max_iters=100):
        self.normalize()
        seed = seed - self.base

        q = np.zeros((self.n, 1))
        if seed < 0 or seed >= self.n:
            raise ValueError('Out of range of seed node id')

        q[seed] = 1.0

        r, residuals = iterator.iterate(self.nAT, q, c, epsilon,
                max_iters)

        return r
