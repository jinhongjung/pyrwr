# pyrwr
**Py**thon Implementation for **R**andom **W**alk with **R**estart (PyRWR).  

Random Walk with Restart (RWR) is one of famous link analysis algorithms, which measures node-to-node proximities in arbitrary types of graphs (networks).
The representative applications include various real-world graph mining tasks such as personalized node ranking, recommendation in graphs (e.g., 'who you may know'), and anormaly detection.  

`pyrwr` aims to implement algorithms for computing RWR scores in Python based on numpy and scipy.
More specifically, `pyrwr` focuses on computing a single source RWR score vector w.r.t. a given query (seed) node, which is used for a personalized ranking of the node. 
Besides RWR, `pyrwr` supports computing Personalized PageRank (PPR) and PageRank which are well-known variants of RWR.

The supported features of `pyrwr` are:
* Query types (see the details in [])
	- Random Walk with Restart (RWR): personalized ranking; only a single seed is allowed
	- Personalized PageRank (PPR): personalized ranking; multiple seeds are allowed
	- PageRank: global ranking; all nodes are used as seeds
* Graph types (see the details in [])
	- Unweighted/weighted graphs
	- Directed graphs
	- Undirected graphs (not yet, coming soon)
	- Bipartite networks (not yet, coming soon)
* Algorithm types (see the details in [])
	- Power iteration (default, exact as anytime algorithms)
	- Forward push (approximate, not yet)

### Caution
**This repository is currentely under development and testing!**
**Updates will continue after February!**

- If you are interested in studying random walk based ranking models such as PageRank and RWR, please consider this tutorial (https://github.com/jinhongjung/tutorial-on-link-analysis) that provides how to correctly implement the algorithms of those model in Python and to analyze real-world networks using those ranking models.

## Installation [currently not suppported]
To install this package, type the following:
```bash
cd pyrwr
pip install -r requirements.txt
python setup.py install
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

## Usage
We provide the following simple command line usage:
```bash
pyrwr --query-type rwr --input-path data/sample.tsv --output-path output/scores.tsv --seeds 987
```
This will compute an RWR score vector w.r.t. the seed node given by `--seeds` in the given graph specified by `--input-path`, and write the vector into the target file in `--output-path`. `--query-type` specifies the type of query, e.g., this example indicates an RWR query.
The detailed format of the input and output files is described below.

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
The above example represents an unweighted graph where each line indicates an edge from source to target. 
In this case, the edge weight is set to 1 uniformly. 
To vary weights edge by edge, use the following format:

```
# format: source (int) \t target (int) \t weight (float)
1	2	1.5	
1	4	3.5
2	3	6.0
...
```
Note that RWR is defined on positively weighted networks; thus, only positive weights are allowed. 


### Output Format
The default output of `pyrwr` contains the single source RWR score vector w.r.t. the given seed node as follows:
```
# format : an RWR score of i-th node
0.1232e-3
0.0349e-4
...
```

## How to Use `pyrwr` in My Codes?
The following example shows how to import `pyrwr` and compute an RWR query.

```python
from pyrwr.rwr import RWR

rwr = RWR()
rwr.read_graph(input_graph)
r = rwr.compute(seed, c, epsilon, max_iters)
```
Note that `seed` should be `int`. The format of the file at `input_graph` should follow one of the above input formats.
`r` is a column vector (ndarray) having the RWR score vector w.r.t. `seed` node.
The shape of `r` will be (n, 1) where `n` is the number of nodes.

For a PPR query, see the following code:
```python
from pyrwr.ppr import PPR

ppr = PPR()
ppr.read_graph(input_graph)
r = ppr.compute(seeds, c, epsilon, max_iters)
```
In this case, `seeds` is the list of seeds. `r` is the PPR score vector w.r.t. `seeds`.
Note that the PPR vector `r` is used for obtaining the personalized node ranking list related to all seeds in the `seeds` list.

For the PageRank query, use the following snippet:
```python
from pyrwr.pagerank import PageRank

pagerank = PageRank()
pagerank.read_graph(input_graph)
r = pagerank.compute(c, epsilon, max_iters)
```
Note that for `pagerank`, we do not need to specify seeds since PageRank is a global ranking; thus, it automatically sets required seeds (i.e., all nodes are used as seeds).


## Arguments of `pyrwr`
We summarize the input arguments of `pyrwr` in the following table:

| Arguments     | Query Type | Explanation       | Default       | 
| --------------|:------:|-------------------|:-------------:|
| `query-type` | `common` | Query type among [rwr, ppr, pagerank] | `None`|
| `input-path` | `common` | Input path for a graph | `None`|
| `output-path` | `common` | Output path for storing a query result | `None`|
| `seeds` | `rwr` | A single seed node id | `None`|
| `seeds` | `ppr` | File path for seeds (`str`) or list of seeds (`list`) | `[]`|
| `c` | `common` | Restart probablity (`rwr`) or jumping probability (otherwise) | `0.15`|
| `epsilon` | `common` | Error tolerance for power iteration | `1e-9`|
| `max-iters` | `common` | Maximum number of iterations for power iteration | `100`|
| `handles_deadend` | `common` | If true, handles the deadend issue | `True`|

The value of `Query Type` in the above table is one of the followings:
* `common`: parameter of all of `rwr`, `ppr`, and `pagerank`
* `rwr`: parameter of `rwr`
* `ppr`: parameter of `ppr`
* `pagerank`: parameter of `pagerank`

Note the followings:
* If you want to compute `pagerank` query, then do not need to specify `seeds`.
* For directed graphs, there might be deadend nodes whose outdegree is zero. In this case, a naive power iteration would incur leaking out scores. 
`handles_deadend` exists for such issue handling deadend nodes. With `handles_deadend`, you can guarantee that the sum of a score vector is 1.
Otherwise, the sum would less than 1 in directed graphs. 
The strategy `pyrwr` exploits is that whenever a random surfer visits a deadend node, go back to a seed node (or one of seed nodes), and restart.
See this for the detailed technique of the strategy.

## Todo
- [x] to implement a function for reading an input graph
- [x] to implement a class for computing RWR
	- [x] row-normalization
	- [x] power-iteration
	- [x] rwr
	- [x] ppr
	- [x] pagerank
- [x] to process users' arguments from command lines (python-fire)
	- [ ] to update it if necessary
	- [ ] to write a result to a file
- [ ] to support the following graph types:
	- [x] directed graph
	- [x] unweighted graph/weighted graph
	- [x] directed graph having deadend nodes
	- [x] undirected graph
	- [ ] bipartite network
- [ ] to add conditional statements for checking the following
	- [x] is the graph positively weighted?
	- [x] is the given seed's id out of range?
	- [x] is the format of the given data invalid?
	- [ ] does the graph contain deadend nodes?
	- [x] is the range of node ids invalid?
- [ ] to perform tests on various settings
	- [ ] tests on unwiehgted & directed graphs
	- [ ] tests on unweighted & undirected graphs
	- [ ] tests on weighted & directed graphs
	- [ ] tests on weighted & undirected graphs
	- [ ] tests on deadend nodes
- [ ] to add logging with logger and tqdm
	- [ ] to add logger
	- [x] to polish tqdm things
- [x] to add comments
- [ ] to prepare setup process
- [x] to write documents
