import numpy as np
from numpy.linalg import norm
from tqdm import tqdm, trange

def iterate(A, q, c=0.15, epsilon=1e-6,
        max_iters=100, handles_deadend=True, norm_type=1):
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
    x = q
    old_x = q
    residuals = np.zeros((max_iters, 1))

    pbar = tqdm(total=max_iters, leave=False)
    for i in range(max_iters):
        if handles_deadend:
            x = (1-c)*(A.dot(old_x))
            S = np.sum(x)
            x = x + (1-S)*q
        else:
            x = (1-c)*(A.dot(old_x)) + c*q

        residuals[i] = norm(x - old_x, norm_type)
        pbar.set_description("Residual at %d-iter: %e" % (i, residuals[i]))

        if residuals[i] <= epsilon:
           pbar.set_description("Scores have converged")
           pbar.update(max_iters)
           break

        old_x = x
        pbar.update(1)
    pbar.close()

    return x, residuals[0:i+1]
