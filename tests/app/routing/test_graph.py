import unittest
import pandas as pd
from shapely.geometry import Point
from app.app.routing.graph import Graph


class GraphTest(unittest.TestCase):

    def test_adjacent_list(self):
        nodes, edges = self.__get_nodes_and_edges()
        graph = Graph(nodes, edges)

        self.assertEqual(4, len(graph.nodes.index))
        self.assertEqual(4, len(graph.graph))
        self.assertEqual({'N4', 'N2'}, set(graph.graph['N1'].neighbors.keys()))
        self.assertEqual({'N1', 'N3'}, set(graph.graph['N2'].neighbors.keys()))
        self.assertEqual({'N2', 'N4'}, set(graph.graph['N3'].neighbors.keys()))
        self.assertEqual({'N3', 'N1'}, set(graph.graph['N4'].neighbors.keys()))

    def test_closest_point(self):
        search_point = Point(13.29, 52.39)
        nodes, edges = self.__get_nodes_and_edges()
        graph = Graph(nodes, edges)
        closest = graph.get_closest(search_point)
        self.assertEqual(13.3, closest.iloc[0].geometry.x)
        self.assertEqual(52.4, closest.iloc[0].geometry.y)
        self.assertEqual('N3', closest.index.values[0])

    @staticmethod
    def __get_nodes_and_edges():
        node_data = [['N1', 52.3, 13.4], ['N2', 52.4, 13.4], ['N3', 52.4, 13.3], ['N4', 52.3, 13.3]]
        edge_data = [['N1', 'N2', 30], ['N2', 'N3', 20], ['N3', 'N4', 45], ['N4', 'N1', 25]]
        nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
        nodes.set_index('id', inplace=True)
        edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
        return nodes, edges


if __name__ == '__main__':
    unittest.main()
