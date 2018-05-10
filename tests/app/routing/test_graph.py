import unittest
from shapely.geometry import Point
from tests.app.helpers import get_test_graph


class GraphTest(unittest.TestCase):

    def setUp(self):
        self.graph = get_test_graph()
        self.closest = self.graph.get_closest(Point(13.29, 52.39))
        self.coordinate = self.graph.get_coordinate('N3')

    def test_number_of_nodes_in_data_frame(self):
        self.assertEqual(4, len(self.graph.nodes.index))

    def test_number_of_nodes_in_adjacent_list(self):
        self.assertEqual(4, len(self.graph.graph))

    def test_neighbors_of_first_node_in_adjacent_list(self):
        self.assertEqual({'N4', 'N2'}, set(self.graph.graph['N1'].neighbors.keys()))

    def test_neighbors_of_second_node_in_adjacent_list(self):
        self.assertEqual({'N1', 'N3'}, set(self.graph.graph['N2'].neighbors.keys()))

    def test_neighbors_of_third_node_in_adjacent_list(self):
        self.assertEqual({'N2', 'N4'}, set(self.graph.graph['N3'].neighbors.keys()))

    def test_neighbors_of_fourth_node_in_adjacent_list(self):
        self.assertEqual({'N3', 'N1'}, set(self.graph.graph['N4'].neighbors.keys()))

    def test_get_closest_point_longitude(self):
        self.assertEqual(13.3, self.closest.iloc[0].geometry.x)

    def test_get_closest_point_latitude(self):
        self.assertEqual(52.4, self.closest.iloc[0].geometry.y)

    def test_get_closest_point_index(self):
        self.assertEqual('N3', self.closest.index.values[0])

    def test_get_coordinate_by_id_longitude(self):
        self.assertEqual(13.3, self.coordinate.iloc[0].geometry.x)

    def test_get_coordinate_by_id_latitude(self):
        self.assertEqual(52.4, self.coordinate.iloc[0].geometry.y)

    def test_get_coordinate_by_id_index(self):
        self.assertEqual('N3', self.coordinate.index.values[0])


if __name__ == '__main__':
    unittest.main()
