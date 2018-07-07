# pyrwr
Python Implementation for Random Walk with Restart (RWR).  

`RWR` is one of famous link analysis algorithms, which measures node-to-node proximities in arbitrary types of graphs (networks).
The representative applications include various real-world graph mining tasks such as personalized node ranking, recommendation in graphs such as 'who you may know', and anormaly detection.
`pyrwr` aims to implement algorithms for computing `RWR` scores in Python.
More specifically, `pyrwr` focuses on computing a single source RWR score vector w.r.t. a given query (seed) node, which is used for a personalized ranking of the node. 

## Caution
**This repository is currentely under development and testing!**

# Usage
We provide the following simple command line usage:
```bash
pyrwr --input-path data/sample.tsv --output-path output/scores.tsv --seed 987
```
This will compute an RWR score vector w.r.t. the given seed node `--seed` in the given graph specified by `--input-path`, and write the vector into the target file in `--output-path`.
The detailed format of the input and output files is described below.

# Input and Output Format

## Input Format
The default input of `pyrwr` represents the edge list of a graph with the following format (tab separated):
```
# format: source \t target
0	1
2	3
1	4
...
```

## Output Format
The default output of `pyrwr` contains the single source RWR score vector w.r.t. the given seed node as follows:
```
# format : an RWR score
0.1232e-3
0.2349e-4
...
```

# Todo
- [x] to implement a function for reading an input graph
- [x] to implement a class for computing RWR
	- [x] row-normalization
	- [x] power-iteration
	- [x] rwr
	- [ ] ppr
	- [ ] pagerank
- [x] to process users' arguments from command lines (python-fire)
	- [ ] to update it if necessary
	- [ ] to write a result to a file
- [ ] to support the following graph types:
	- [x] directed graph
	- [x] unweighted graph/weighted graph
	- [x] directed graph having deadend nodes
	- [ ] undirected graph
	- [ ] bipartite network
- [ ] to add conditional statements for checking the following
	- [ ] is the graph positively weighted?
	- [ ] is the given seed's id out of range?
	- [ ] is the format of the given data invalid?
	- [ ] does the graph contain self-looped nodes?
	- [ ] does the graph contain deadend nodes?
	- [ ] is the range of node ids invalid?
- [ ] to perform tests on various settings
	- [ ] tests on unwiehgted & directed graphs
	- [ ] tests on unweighted & undirected graphs
	- [ ] tests on weighted & directed graphs
	- [ ] tests on weighted & undirected graphs
	- [ ] tests on deadend nodes
- [ ] to add logging with logger and tqdm
	- [ ] to polish tqdm things
- [ ] to add comments
- [ ] to write documents
