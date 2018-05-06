import unittest
import pandas as pd
from shapely.geometry import Polygon
from app.app.routing.graph import Graph
from app.app.routing.edge import Edge


class EdgeTest(unittest.TestCase):

    def test_edge_creation(self):
        expected = Polygon(((13.4, 52.3), (13.4, 52.3), (13.3, 52.3), (13.3, 52.3)))
        node_data = [['N1', 52.3, 13.4], ['N2', 52.4, 13.4], ['N3', 52.4, 13.3], ['N4', 52.3, 13.3]]
        edge_data = [['N1', 'N2', 30], ['N2', 'N3', 20], ['N3', 'N4', 20], ['N4', 'N1', 25]]
        nodes_df = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
        nodes_df.set_index('id', inplace=True)
        edges_df = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
        g = Graph(nodes_df, edges_df)
        edge = Edge(g.graph['N4'], g.graph['N1'])

        self.assertEqual(25, edge.distance)
        self.assertEqual(0.0, edge.azimuth)
        self.assertTrue(expected.difference(edge.bounding_box).is_empty)
