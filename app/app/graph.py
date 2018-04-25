import pandas as pd
import random
from geopandas import GeoDataFrame
from shapely.geometry import Point


class Graph:

    def __init__(self, nodes, edges):
        self.nodes = self.__create_nodes(nodes)
        self.adjacent = self.__create_adjacent(edges)

    @classmethod
    def load_default(cls):
        nodes = pd.read_pickle("../../resources/nodes.p")
        edges = pd.read_pickle("../../resources/edges.p")
        return Graph(nodes, edges)

    def next_edge(self, previous_start, previous_end):
        start = self.node_by_id(previous_end)
        end_id = self.__seed_end_node(previous_end, previous_start)
        end = self.node_by_id(end_id)
        return start.geometry, end.geometry, previous_end, end_id

    def seed(self):
        start = self.__seed_start_node()
        start_id = start.index.values[0]
        end_id = self.__seed_end_node(start_id)
        end = self.node_by_id(end_id)
        return start.iloc[0].geometry, end.geometry, start_id, end_id

    def node_by_id(self, node_id):
        return self.nodes.loc[node_id]

    def __seed_start_node(self):
        return self.nodes.sample(n=1)

    def __seed_end_node(self, node, exclude=None):
        neighbors = self.adjacent[node][:]
        if exclude is not None and exclude in neighbors and len(neighbors) > 1:
            neighbors.remove(exclude)
        return random.choice(neighbors)

    @staticmethod
    def __create_nodes(nodes):
        geometry = [Point(xy) for xy in zip(nodes.lat, nodes.lon)]
        nodes = GeoDataFrame(nodes.drop(['lat', 'lon'], axis=1),
                             crs={'init': 'epsg:4326'},
                             geometry=geometry)
        return nodes

    @staticmethod
    def __create_adjacent(edges):
        copy = edges.copy(deep=True)
        copy.columns = ['node2', 'node1', 'distance']
        edges = pd.concat([edges, copy]).reset_index()[['node1', 'node2', 'distance']]
        adjacent = edges.node1.groupby(edges.node2).apply(list)
        return {i: row for i, row in adjacent.iteritems()}


if __name__ == '__main__':
    graph = Graph.load_default()
    print(graph.adjacent)
