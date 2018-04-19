import pandas as pd


class Graph:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.nodes.set_index('id', inplace=True)
        copy = edges.copy(deep=True)
        copy.columns = ['node2', 'node1', 'distance']
        self.edges = pd.concat([edges, copy]).reset_index()[['node1', 'node2', 'distance']]
        self.adjacent = self.edges.node1.groupby(self.edges.node2).apply(list)

    def seed(self):
        node = self.__seed_node()
        edge = self.__seed_edge(node)
        return node, edge

    def __seed_node(self):
        return self.nodes.sample(n=1)

    def __seed_edge(self, node):
        return self.edges[self.edges.node1 == node.index.values[0]].sample(n=1)


if __name__ == '__main__':
    loaded_nodes = pd.read_pickle("../../resources/nodes.p")
    loaded_edges = pd.read_pickle("../../resources/edges.p")
    graph = Graph(loaded_nodes, loaded_edges)
    print(graph.adjacent)
