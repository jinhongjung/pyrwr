import sys
from utils import reader
from pyrwr.rwr import RWR
import numpy as np

def main():
    data = './data/sample.tsv'
    A = reader.read_graph(data)
    rwr = RWR(A)

    s = 989
    c = 0.0001
    epsilon = 1e-30
    max_iters = 3000
    r = rwr.compute(s, c, epsilon, max_iters)
    print(np.sum(r))

if __name__ == "__main__":
    sys.exit(main())
