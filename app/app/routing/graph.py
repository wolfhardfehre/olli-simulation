import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.ops import nearest_points
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app.routing.node import Node


class Graph:
    instance = None

    def __init__(self, nodes, edges):
        self.nodes = self.__prepare_nodes(nodes)
        edges = self.__prepare_edges(edges)
        joined = self.__join(edges, self.nodes)
        self.graph = self.__adjacent(joined)

    @classmethod
    def load_default(cls):
        if cls.instance is None:
            nodes = pd.read_pickle("./resources/nodes.p")
            edges = pd.read_pickle("./resources/edges.p")
            cls.instance = Graph(nodes, edges)
        return cls.instance

    def get_closest(self, search_point):
        nearest = self.nodes['geometry'] == nearest_points(search_point, self.nodes.unary_union)[1]
        return self.nodes[nearest]

    def get_closest_node(self, search_point):
        return self.graph[self.get_closest(search_point).index[0]]

    def get_coordinate(self, id):
        return self.nodes.loc[[id]]

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
        """
        Creates a adjacent dict of nodes with their neighbors.

        Parameters
        ----------
        joined: DataFrame
            containing edges with origin, destination node, the distance between
            and their corresponding geometries.

        Returns
        -------
        dict containing node ids as keys and corresponding nodes as values.

        """
        adjacent = {}
        for idx, row in joined.iterrows():
            index, geom = row.node1, row.geometry
            if index not in adjacent:
                adjacent[index] = Node(index, geom)
            adjacent.get(index).add_neighbor(row.node2, row.distance)
        return adjacent


if __name__ == '__main__':
    g = Graph.load_default()
    search_point = Point(13.3587658,52.4857809)
    closest = g.get_closest(search_point)
    print(closest)

    coordinate = g.get_coordinate(27785378)
    print(coordinate)
