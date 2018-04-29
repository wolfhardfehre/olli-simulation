import random
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from app.app.routing.node import Node


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = self.__prepare_nodes(nodes)
        edges = self.__prepare_edges(edges)
        joined = self.__join(edges, self.nodes)
        self.graph = self.__adjacent(joined)

    @classmethod
    def load_default(cls):
        nodes = pd.read_pickle("./resources/nodes.p")
        edges = pd.read_pickle("./resources/edges.p")
        return Graph(nodes, edges)

    def seed(self):
        start_id = random.choice(list(self.graph.keys()))
        return self.next_edge(None, start_id)

    def next_edge(self, previous_start_id, previous_end_id):
        start = self.graph[previous_end_id]
        end_id = self.__seed_end_node(previous_end_id, previous_start_id)
        end = self.graph[end_id]
        return start.geometry, end.geometry, previous_end_id, end_id

    def __seed_end_node(self, node, exclude=None):
        neighbors = list(self.graph[node].neighbors.keys())
        if exclude is not None and exclude in neighbors and len(neighbors) > 1:
            neighbors.remove(exclude)
        return random.choice(neighbors)

    @staticmethod
    def __prepare_nodes(nodes):
        geometry = [Point(xy) for xy in zip(nodes.lat, nodes.lon)]
        nodes = GeoDataFrame(nodes.drop(['lat', 'lon'], axis=1), crs={'init': 'epsg:4326'}, geometry=geometry)
        return nodes

    @staticmethod
    def __prepare_edges(edges):
        copy = edges.copy(deep=True)
        copy.columns = ['node2', 'node1', 'distance']
        return pd.concat([edges, copy]).reset_index()[['node1', 'node2', 'distance']]

    @staticmethod
    def __join(edges, nodes):
        edges = edges.join(nodes, on='node1', rsuffix='_from')
        edges = edges.join(nodes, on='node2', rsuffix='_to')
        return edges

    @staticmethod
    def __adjacent(joined):
        adjacent = {}
        for idx, row in joined.iterrows():
            index, geom = row.node1, row.geometry
            if index not in adjacent:
                adjacent[index] = Node(index, geom)
            adjacent.get(index).add_neighbor(row.node2, row.distance)
        return adjacent
