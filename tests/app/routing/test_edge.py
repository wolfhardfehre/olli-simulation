import unittest
from shapely.geometry import Polygon
from app.app.routing.edge import Edge
from tests.app.helpers import get_test_graph


class EdgeTest(unittest.TestCase):

    def setUp(self):
        graph = get_test_graph()
        self.edge = Edge(graph.graph['N4'], graph.graph['N1'])

    def test_edge_distance(self):
        self.assertEqual(25, self.edge.distance)

    def test_edge_azimuth(self):
        self.assertEqual(0.0, self.edge.azimuth)

    def test_edge_bounding_box(self):
        expected = Polygon(((13.4, 52.3), (13.4, 52.3), (13.3, 52.3), (13.3, 52.3)))
        self.assertTrue(expected.difference(self.edge.bounding_box).is_empty)
