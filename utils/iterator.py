import numpy as np
from numpy.linalg import norm
from tqdm import tqdm, trange

def iterate(A, q, c=0.15, epsilon=1e-6,
        max_iters=100, handles_deadend=True, norm_type=1):
    """
    """
    x = q
    old_x = q
    residuals = np.zeros((max_iters, 1))

    pbar = trange(max_iters)
    for i in pbar:
        if handles_deadend:
            x = (1-c)*(A.dot(old_x))
            S = np.sum(x)
            x = x + (1-S)*q
        else:
            x = (1-c)*(A.dot(old_x)) + c*q

        residuals[i] = norm(x - old_x, norm_type)
        pbar.set_description("Residual at %d-iter: %e"
                % (i, residuals[i]))

        if residuals[i] <= epsilon:
           break

        old_x = x

    return x, residuals
