import sys
import os.path
import fire
import types
from pyrwr.rwr import RWR
from pyrwr.ppr import PPR
from pyrwr.pagerank import PageRank
import numpy as np

def process_query(query_type, graph_type, input_path, output_path, seeds=[], c=0.15,
        epsilon=1e-9, max_iters=100, handles_deadend=True):
    '''
    Processed a query to obtain a score vector w.r.t. the seeds

    inputs
        query_type : str
            type of querying {'rwr', 'ppr', 'pagerank'}
        graph_type: : str
            type of graph {'directed', 'undirected', 'bipartite'}
        input_path : str
            path for the graph data
        output_path : str
            path for storing an RWR score vector
        seeds : str
            seeds for query
                - 'rwr' : just a nonnegative integer
                - 'ppr' : list of nonnegative integers or file path
                - 'pagerank' : None, seeds = range(0, n)
        c : float
            restart probability
        epsilon : float
            error tolerance for power iteration
        max_iters : int
            maximum number of iterations for power iteration handles_deadend : bool
            if true, it will handle the deadend issue in power iteration
            otherwise, it won't, i.e., no guarantee for sum of RWR scores
            to be 1 in directed graphs
    outputs
        r : ndarray
            RWR score vector
    '''

    if query_type == 'rwr':
        if type(seeds) is not int:
            raise TypeError('Seeds should be a single integer for RWR')
        rwr = RWR()
        rwr.read_graph(input_path, graph_type)
        r = rwr.compute(int(seeds), c, epsilon, max_iters)
    elif query_type == 'ppr':
        seeds = get_seeds(seeds)
        ppr = PPR()
        ppr.read_graph(input_path, graph_type)
        r = ppr.compute(seeds, c, epsilon, max_iters)
    elif query_type == 'pagerank':
        pagerank = PageRank()
        pagerank.read_graph(input_path, graph_type)
        r = pagerank.compute(c, epsilon, max_iters)

    write_vector(output_path, r)

def get_seeds(seeds):
    if type(seeds) is str:
        _seeds = []
        with open(seeds, 'r') as f:
            _seeds = [int(seed) for seed in f]
    elif type(seeds) is list:
        _seeds = [int(seed) for seed in seeds]
    else:
        raise TypeError('Seeds for PPR should be list or file path')

    return _seeds

def write_vector(output_path, r):
    with open(output_path, 'w') as f:
        np.savetxt(output_path, r)


def main():
    fire.Fire(process_query)


if __name__ == "__main__":
    sys.exit(main())
