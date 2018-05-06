import unittest
from unittest.mock import patch
import pandas as pd
from app.app.routing.dijkstra import shortest_path
from app.app.routing.graph import Graph
from app.app.entities.route import Route


class RouteTest(unittest.TestCase):

    @patch('app.app.entities.tour.Tour')
    @patch('app.app.entities.models.velocity_model.VelocityModel')
    def test_route_creation(self, mock_tour, mock_velocity):
        start = '1'
        end = '3'
        nodes, edges = self.get_nodes_and_edges()
        graph = Graph(nodes, edges)
        path = shortest_path(graph.graph, start, end)

        route = Route(graph.graph, path, mock_tour, mock_velocity)

        assert False

    @staticmethod
    def get_nodes_and_edges():
        node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
        edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 20], ['4', '1', 25]]
        nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
        nodes.set_index('id', inplace=True)
        edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
        return nodes, edges
