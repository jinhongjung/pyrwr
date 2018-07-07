from utils import reader, normalizer, iterator

class PyRWR:
    normalized = False

    def __init__(self):
        pass

    def read_graph(self, input_path):
        '''
        Read a graph from the edge list at input_path

        inputs
            input_path : str
                path for the graph data
        '''

        self.A, self.base = reader.read_graph(input_path)
        self.m, self.n = self.A.shape
        self.normalize()

    def normalize(self):
        '''
        Perform row-normalization of the adjacency matrix
        '''
        if self.normalized == False:
            nA = normalizer.row_normalize(self.A)
            self.nAT = nA.T
            self.normalized = True
