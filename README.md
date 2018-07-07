# pyrwr
Python Implementation for Random Walk with Restart (RWR). 

# Todo
- [x] to implement a function for reading an input graph
- [x] to implement a class for computing RWR
	- [x] row-normalization
	- [x] power-iteration
	- [x] rwr
	- [ ] ppr
	- [ ] pagerank
- [x] to process users' arguments from command lines (python-fire)
	- [ ] to update if necessary
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
- [ ] to add logger
- [ ] to add comments
- [ ] to write documents
