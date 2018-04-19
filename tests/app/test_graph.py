import unittest
import pandas as pd

from app.app.graph import Graph


class GraphTest(unittest.TestCase):

    def test_adjacent_list(self):
        expected = [['4', '2'], ['1', '3'], ['2', '4'], ['3', '1']]
        node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
        edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 45], ['4', '1', 25]]
        nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
        nodes.set_index('id')
        edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
        graph = Graph(nodes, edges)

        self.assertEqual(4, len(graph.nodes.index))
        self.assertEqual(8, len(graph.edges.index))
        [self.assertEqual(results, elements) for results, elements in zip(expected, graph.adjacent)]


if __name__ == '__main__':
    unittest.main()
