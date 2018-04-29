import random
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.ops import nearest_points
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

    def get_closest(self, search_point):
        return nearest_points(search_point, self.nodes.unary_union)[1]

    def __seed_end_node(self, node, exclude=None):
        neighbors = list(self.graph[node].neighbors.keys())
        if exclude is not None and exclude in neighbors and len(neighbors) > 1:
            neighbors.remove(exclude)
        return random.choice(neighbors)

    @staticmethod
    def __prepare_nodes(nodes):
        geometry = [Point(xy) for xy in zip(nodes.lon, nodes.lat)]
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


if __name__ == '__main__':
    node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
    edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 20], ['4', '1', 25]]
    nodes_df = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
    nodes_df.set_index('id', inplace=True)
    edges_df = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
    g = Graph(nodes_df, edges_df)
    search_point = Point(52.39, 13.29)
    closest = g.get_closest(search_point)
    print(closest.x, closest.y)
