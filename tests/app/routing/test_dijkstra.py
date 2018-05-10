import unittest
from app.app.routing.dijkstra import shortest_path
from tests.app.helpers import get_test_graph


class DijkstraTest(unittest.TestCase):

    def test_shortest_path(self):
        graph = get_test_graph()
        shortest = shortest_path(graph.graph, 'N1', 'N3')

        self.assertEqual(['N1', 'N4', 'N3'], shortest)
