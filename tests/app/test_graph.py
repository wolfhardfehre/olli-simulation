import unittest
import pandas as pd

from app.app.graph import Graph


class GraphTest(unittest.TestCase):

    def test_adjacent_list(self):
        node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
        edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 45], ['4', '1', 25]]
        nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
        nodes.set_index('id')
        edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
        graph = Graph(nodes, edges)

        self.assertEqual(4, len(graph.nodes.index))
        self.assertEqual(4, len(graph.adjacent))
        self.assertEqual(['4', '2'], graph.adjacent['1'])
        self.assertEqual(['1', '3'], graph.adjacent['2'])
        self.assertEqual(['2', '4'], graph.adjacent['3'])
        self.assertEqual(['3', '1'], graph.adjacent['4'])


if __name__ == '__main__':
    unittest.main()