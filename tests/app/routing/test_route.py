import unittest
from app.app.routing.route import Route
from app.app.routing.node import Node
from shapely.geometry import Point, LineString


class RouteTest(unittest.TestCase):

    def test_route(self):
        nodes = [
            Node('1', Point(13.123, 54.486)),
            Node('2', Point(13.124, 54.456)),
            Node('3', Point(13.125, 54.466))
        ]
        route = Route(nodes)

        self.assertEqual(route.vertex_list, nodes)