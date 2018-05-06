import unittest
from shapely.geometry import Point
from app.app.routing.node import Node


class NodeTest(unittest.TestCase):

    def test_node_creation(self):
        point = Point(0, 0)

        node = Node(1, point)

        self.assertEqual(1, node.node_id)
        self.assertEqual(point, node.geometry)
        self.assertFalse(node.neighbors)

    def test_adding_neighbor(self):
        point = Point(0, 0)

        node = Node(1, point)
        node.add_neighbor(2, 63)

        self.assertEqual(1, node.node_id)
        self.assertEqual(point, node.geometry)
        self.assertTrue(node.neighbors)
        self.assertEqual(63, node.neighbors[2])
