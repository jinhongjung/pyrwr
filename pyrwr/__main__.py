import sys
import os.path
import fire
from pyrwr.rwr import RWR
import numpy as np

def process_query(input_path, output_path, seed, c=0.15, epsilon=1e-9,
        max_iters=100, handles_deadend=True):
    '''
    Computes a single source RWR score vector w.r.t. a given seed.

    inputs
        input_path : str
            path for the graph data
        output_path : str
            path for storing an RWR score vector
        seed : int
            seed (query) node id
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
            RWR score vector

    '''

    rwr = RWR()
    rwr.read_graph(input_path)
    r = rwr.compute(seed, c, epsilon, max_iters)
    write_vector(output_path, r)
    #print(np.sum(r))


def write_vector(output_path, r):
    with open(output_path, 'w') as f:
        np.savetxt(output_path, r)


def main():
    fire.Fire(process_query)


if __name__ == "__main__":
    sys.exit(main())
