#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy.linalg import norm
from tqdm import tqdm
import torch
import warnings
import time

# This aims to disable UserWarning incurred by torch's Sparse CSR which is in beta state.
warnings.filterwarnings("ignore")


def iterate(A,
            q,
            c=0.15,
            epsilon=1e-9,
            max_iters=100,
            handles_deadend=True,
            norm_type=1,
            device="cpu"):
    """
    Perform power iteration for RWR, PPR, or PageRank

    inputs
        A : csr_matrix
            input matrix (for RWR and it variants, it should be row-normalized)
        q : ndarray
            query vector
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
        norm_type : int
            type of norm used in measuring residual at each iteration
    outputs
        x : ndarray
            result vector
    """
    if device == "cpu":
        return iterate_cpu(A, q, c, epsilon, max_iters, handles_deadend, norm_type)
    elif device == "gpu":
        return iterate_gpu(A, q, c, epsilon, max_iters, handles_deadend, norm_type)
    else:
        raise TypeError("device should be cpu or gpu")


def iterate_cpu(A,
                q,
                c=0.15,
                epsilon=1e-9,
                max_iters=100,
                handles_deadend=True,
                norm_type=1):
    """
    This performs power iteration using numpy on a single cpu
    """
    device = torch.device("cpu")
    x = q
    old_x = q
    residuals = np.zeros(max_iters)

    pbar = tqdm(total=max_iters)
    i = 0
    for i in range(max_iters):
        if handles_deadend:
            x = (1 - c) * (A.dot(old_x))
            S = np.sum(x)
            x = x + (1 - S) * q
        else:
            x = (1 - c) * (A.dot(old_x)) + (c * q)

        residuals[i] = norm(x - old_x, norm_type)
        pbar.set_description("Residual at %d-iter: %e" % (i, residuals[i]))

        if residuals[i] <= epsilon:
            pbar.set_description("The iteration has converged at %d-iter" % (i))
            break

        old_x = x
        pbar.update(1)

    pbar.close()

    return x, residuals[0:i + 1]


def iterate_gpu(A,
                q,
                c=0.15,
                epsilon=1e-9,
                max_iters=100,
                handles_deadend=True,
                norm_type=1):
    """
    This performs power iteration using torch on a single gpu
    """
    if not torch.cuda.is_available():
        raise TypeError("cuda is not available. try to use cpu")

    device = torch.device("cuda")

    # convert scipy.csr_matrix to torch's csr matrix
    # - torch.sparse_csr_tensor seems to have a bug that it doesn't correctly convert given inputs
    # - alternatively, we use sparse_coo_tensor(), and convert it using to_sparse_csr()
    start = time.time()
    shaping = A.shape
    A = A.tocoo()
    indices = torch.from_numpy(np.vstack((A.row, A.col)).astype(np.int64))
    values = torch.from_numpy(A.data)
    A = torch.sparse_coo_tensor(indices, values, shaping).to(device)
    A = A.to_sparse_csr()
    residuals = torch.from_numpy(np.zeros(max_iters)).to(device)
    q = torch.from_numpy(q).to(device)
    if not handles_deadend:
        q = q.view(-1, 1) # for using torch.sparse.addmm in one line
    data_elapsed = time.time() - start
    print("Sending data to gpu takes {:.4} sec".format(data_elapsed))

    x = q
    old_x = q

    with torch.no_grad():
        pbar = tqdm(total=max_iters)
        i = 0
        for i in range(max_iters):
            if handles_deadend:
                x = (1 - c) * torch.mv(A, old_x)
                S = torch.sum(x)
                x = x + ((1 - S) * q)
            else:
                # the below computes x = (1 - c) * (A.dot(old_x)) + (c * q)
                x = torch.sparse.addmm(q, A, old_x, beta=c, alpha=(1-c))

            residuals[i] = torch.norm(x - old_x, p=norm_type)
            pbar.set_description("Residual at %d-iter: %e" % (i, residuals[i].item()))

            if residuals[i] <= epsilon:
                pbar.set_description("The iteration has converged at %d-iter" % (i))
                break

            old_x = x
            pbar.update(1)

        pbar.close()
        if not handles_deadend:
            x = x.view(-1)
        x = x.cpu().numpy()
        residuals = residuals.cpu().numpy()

    return x, residuals[0:i + 1]

