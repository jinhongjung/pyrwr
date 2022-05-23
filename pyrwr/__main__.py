#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import fire
import types
from pyrwr.rwr import RWR
from pyrwr.ppr import PPR
from pyrwr.pagerank import PageRank
import numpy as np
import pandas as pd


def process_query(query_type,
                  graph_type,
                  input_path,
                  output_path,
                  seeds=[],
                  c=0.15,
                  epsilon=1e-9,
                  max_iters=100,
                  handles_deadend=True,
                  device="cpu"):
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
            maximum number of iterations for power iteration
        handles_deadend : bool
            if true, it will handle the deadend issue in power iteration
            otherwise, it won't, i.e., no guarantee for sum of RWR scores
            to be 1 in directed graphs
        device : string
            type of computing device {'cpu', 'gpu'}
            default is 'cpu' which will compute a query using numpy
            if it is 'gpu', then it will compute a query using gpu based on pytorch
    outputs
        r : ndarray
            RWR score vector
    '''

    if query_type == 'rwr':
        if type(seeds) is not int:
            raise TypeError('Seeds should be a single integer for RWR')
        rwr = RWR()
        rwr.read_graph(input_path, graph_type)
        r = rwr.compute(int(seeds), c, epsilon, max_iters, handles_deadend, device)
        node_ids = rwr.node_ids
    elif query_type == 'ppr':
        seeds = get_seeds(seeds)
        ppr = PPR()
        ppr.read_graph(input_path, graph_type)
        r = ppr.compute(seeds, c, epsilon, max_iters, handles_deadend, device)
        node_ids = ppr.node_ids
    elif query_type == 'pagerank':
        pagerank = PageRank()
        pagerank.read_graph(input_path, graph_type)
        r = pagerank.compute(c, epsilon, max_iters, handles_deadend, device)
        node_ids = pagerank.node_ids
    else:
        raise TypeError('query_type should be rwr, ppr, or pagerank')

    write_vector(output_path, node_ids, r)
    print_result(node_ids, r)


def print_result(node_ids, r):
    df = pd.DataFrame()
    df['Node'] = node_ids
    df['Score'] = r
    df = df.sort_values(by=['Score'], ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    # print(df[0:10])
    # print(np.sum(r))


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


def write_vector(output_path, node_ids, r):
    data = np.vstack((node_ids, r)).transpose()
    np.savetxt(output_path, data, fmt='%d %e')


def main():
    fire.Fire(process_query)


if __name__ == "__main__":
    sys.exit(main())
