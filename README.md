# pyrwr
**Py**thon Implementation for **R**andom **W**alk with **R**estart (PyRWR).  

Random Walk with Restart (RWR) is one of famous link analysis algorithms, which measures node-to-node proximities in arbitrary types of graphs (networks).
The representative applications include various real-world graph mining tasks such as personalized node ranking, recommendation in graphs (e.g., 'who you may know'), and anormaly detection.  

`pyrwr` aims to implement algorithms for computing RWR scores based on *Power Iteration* using numpy and scipy in Python.
More specifically, `pyrwr` focuses on computing a single source RWR score vector w.r.t. a given query (seed) node, which is used for a personalized node ranking w.r.t. the querying node. 
Besides RWR, `pyrwr` supports computing Personalized PageRank (PPR) with multiple seeds and PageRank which are well-known variants of RWR.

The supported features of `pyrwr` are:
* **Query types**
    - Random Walk with Restart (RWR): personalized ranking; only a single seed is allowed
    - Personalized PageRank (PPR): personalized ranking; multiple seeds are allowed
    - PageRank: global ranking; all nodes are used as seeds
* **Graph types**
    - Unweighted/weighted graphs
    - Undirected/directed graphs
* **GPU computation**
    - If you have a gpu and set `device` to 'gpu', it will process your query on the gpu using pytorch. Once the input data is transformed to the gpu, it computes the query more quickly compared to a cpu. If your graph is large, but fit to the gpu memory, try this option for fast computation.

If you are interested in studying random walk based ranking models such as PageRank and RWR, please consider this hands-on tutorial (https://github.com/jinhongjung/tutorial-on-link-analysis) that provides how to correctly implement the algorithms of those models in Python and to analyze real-world networks using the ranking models.

## Installation
To install this package, type the following:
```bash
cd pyrwr
pip3 install -r requirements.txt
python3 setup.py install
```

These will execute the installation of python modules required by this package. 
The name of the installed program is `pyrwr`. 
If you want to validate whether the installation is successfully finished, type
the following command:
```bash
pyrwr --help
```

### Requirements
* numpy
* scipy
* tqdm
* fire
* pandas
* torch

## Usage
We provide the following simple command line usage:
```bash
pyrwr --query-type rwr --graph-type directed --input-path data/directed/sample.tsv --output-path output/scores.tsv --seeds 10982 --device cpu
```
This will compute an RWR score vector w.r.t. the seed node given by `--seeds` in the given graph specified by `--input-path` on a single cpu, and write the vector into the target file in `--output-path`. `--query-type` specifies the type of query, e.g., this example indicates an RWR query.
The detailed format of the input and output files is described below.

### Example Usage on GPU
```bash
CUDA_VISIBLE_DEVICES=1
pyrwr --query-type rwr --graph-type directed --input-path data/directed/sample.tsv --output-path output/scores.tsv --seeds 10982 --device gpu
```
It tries to compute the rwr query on the gpu whose device id is 1 if the gpu is available. Otherwise, an error will be raised.

## Input and Output Format

### Input Format
The default input of `pyrwr` represents the edge list of a graph with the following format (tab separated):
```
# format: source (int) \t target (int)
1	2
1	4
2	3
...
```
The above example represents an unweighted and directed graph where each line indicates an edge from source to target. 
In this case, the edge weight is set to 1 uniformly. 
The node id should be non-negative (>= 0).
To vary weights edge by edge, use the following format:

```
# format: source (int) \t target (int) \t weight (float)
1	2	1.5	
1	4	3.5
2	3	6.0
...
```
Note that 
* RWR is defined on positively weighted networks; thus, only positive weights are allowed. 
* If there are redundant edges in an weighted network, their weights will be summed, e.g., 
```
# Suppose there are the following redundant edges in the original file.
1   2   3
1   2   5
---------
# Then, their weights are summed in the final adjacency matrix as follows.
1   2   8
```


### Output Format
The default output of `pyrwr` contains the single source RWR score vector w.r.t. the given seed node as follows:
```
# format : node id \t an RWR score of the node
1   0.1232e-3
2   0.0349e-4
...
```

## How to Use `pyrwr` in My Code?
The following example shows how to import `pyrwr` and compute an RWR query.

```python
from pyrwr.rwr import RWR

rwr = RWR()
rwr.read_graph(input_graph, graph_type)
r = rwr.compute(seed, c, epsilon, max_iters)
```
Note that `seed` should be `int`. The format of the file at `input_graph` should follow one of the above input formats.
`r` is a column vector (ndarray) having the RWR score vector w.r.t. `seed` node.
The shape of `r` will be (n, 1) where `n` is the number of nodes.

For a PPR query, see the following code:
```python
from pyrwr.ppr import PPR

ppr = PPR()
ppr.read_graph(input_graph, graph_type)
r = ppr.compute(seeds, c, epsilon, max_iters)
```
In this case, `seeds` is the list of seeds. `r` is the PPR score vector w.r.t. `seeds`.
Note that the PPR vector `r` is used for obtaining the personalized node ranking list related to all seeds in the `seeds` list.

For the PageRank query, use the following snippet:
```python
from pyrwr.pagerank import PageRank

pagerank = PageRank()
pagerank.read_graph(input_graph, graph_type)
r = pagerank.compute(c, epsilon, max_iters)
```
Note that for `pagerank`, we do not need to specify seeds since PageRank is a global ranking; thus, it automatically sets required seeds (i.e., all nodes are used as seeds).


## Arguments of `pyrwr`
We summarize the input arguments of `pyrwr` in the following table:

| Arguments         | Query Type | Explanation | Default       | 
|-------------------|:------:|--|:-------------:|
| `query-type`      | `common` | Query type among [rwr, ppr, pagerank] | `None`|
| `graph-type`      | `common` | Graph type among [directed, undirected] | `None` |
| `input-path`      | `common` | Input path for a graph | `None`|
| `output-path`     | `common` | Output path for storing a query result | `None`|
| `seeds`           | `rwr` | A single seed node id | `None`|
| `seeds`           | `ppr` | File path for seeds (`str`) or list of seeds (`list`) | `[]`|
| `c`               | `common` | Restart probablity (`rwr`) or jumping probability (otherwise) | `0.15`|
| `epsilon`         | `common` | Error tolerance for power iteration | `1e-9`|
| `max-iters`       | `common` | Maximum number of iterations for power iteration | `100`|
| `handles-deadend` | `common` | If true, handles the deadend issue | `True`|
| `device`          | `common` | Computing device [cpu, gpu] | `cpu`|


The value of `Query Type` in the above table is one of the followings:
* `common`: parameter of all of `rwr`, `ppr`, and `pagerank`
* `rwr`: parameter of `rwr`
* `ppr`: parameter of `ppr`
* `pagerank`: parameter of `pagerank`

Note the followings:
* If you want to compute `pagerank` query, then do not need to specify `seeds`.
* For directed graphs, there might be deadend nodes whose out-degree is zero. In this case, a naive power iteration would incur leaking out scores. 
`handles_deadend` exists for such issue handling deadend nodes. With `handles_deadend`, you can guarantee that the sum of a score vector is 1.
Otherwise, the sum would less than 1 in directed graphs. 
The strategy `pyrwr` exploits is that whenever a random surfer visits a deadend node, go back to a seed node (or one of seed nodes), and restart.
See this for the detailed technique of the strategy.
