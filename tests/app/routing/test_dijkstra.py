import unittest
import pandas as pd
from app.app.routing.dijkstra import shortest_path
from app.app.routing.graph import Graph


class DijkstraTest(unittest.TestCase):

    def test_shortest_path(self):
        node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
        edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 20], ['4', '1', 25]]
        nodes_df = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
        nodes_df.set_index('id', inplace=True)
        edges_df = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
        g = Graph(nodes_df, edges_df)

        shortest = shortest_path(g.graph, '1', '3')
        self.assertEqual(['1', '4', '3'], shortest)
