import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from queue import PriorityDict


class Node:
    def __init__(self, node_id, geometry):
        self.node_id = node_id
        self.geometry = geometry
        self.neighbors = {}

    def add_neighbor(self, node_id, distance):
        self.neighbors[node_id] = distance

    def __repr__(self):
        return 'Node[id={}, geom={}, neighbors={}]'.format(self.node_id, self.geometry, self.neighbors)


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = self.__prepare_nodes(nodes)
        edges = self.__prepare_edges(edges)
        joined = self.__join(edges, self.nodes)
        self.graph = self.__adjacent(joined)

    @staticmethod
    def __prepare_nodes(nodes):
        geometry = [Point(xy) for xy in zip(nodes.lat, nodes.lon)]
        nodes = GeoDataFrame(nodes.drop(['lat', 'lon'], axis=1), crs={'init': 'epsg:4326'}, geometry=geometry)
        nodes.set_index('id', inplace=True)
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


def shortest_path(graph, start, end):
    """ Shortest Path by David Eppstein, UC Irvine, 8 Mar 2002 """
    distances, predecessors = dijkstra(graph.graph, start, end)
    path = []
    while 1:
        path.append(end)
        if end == start:
            break
        end = predecessors[end]
    path.reverse()
    return path


def dijkstra(graph, start, end=None):
    """ Dijkstra by David Eppstein, UC Irvine, 8 Mar 2002 """
    distances, predecessors = {}, {}
    priority_dict = PriorityDict()
    priority_dict[start] = 0

    for v in priority_dict:
        distances[v] = priority_dict[v]
        if v == end:
            break

        for w in graph[v].neighbors:
            distance = distances[v] + graph[v].neighbors[w]
            if w in distances:
                if distance < distances[w]:
                    raise ValueError("Dijkstra: found better path to already-final vertex")
            elif w not in priority_dict or distance < priority_dict[w]:
                priority_dict[w] = distance
                predecessors[w] = v

    return distances, predecessors


if __name__ == '__main__':
    node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
    edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 20], ['4', '1', 25]]
    nodes_df = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
    edges_df = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
    g = Graph(nodes_df, edges_df)

    shortest = shortest_path(g, '1', '3')
    print(shortest)
