import sys
import fire
from utils import reader
from pyrwr.rwr import RWR
import numpy as np

def process_query(data_path, seed, c=0.15, epsilon=1e-9,
            max_iters=100, handles_deadend=True):
    '''
    Computes a single source RWR score vector w.r.t. a given seed.

    data_path : str
        path for the graph data
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
    '''
    A = reader.read_graph(data_path)
    rwr = RWR(A)
    r = rwr.compute(seed, c, epsilon, max_iters)
    #print(np.sum(r))

def main():
    fire.Fire(process_query)

if __name__ == "__main__":
    sys.exit(main())
