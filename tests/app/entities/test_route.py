import math
import unittest
from unittest.mock import MagicMock, ANY
from app.app.routing.dijkstra import shortest_path
from app.app.entities.route import Route
from tests.app.helpers import get_test_graph


class RouteTest(unittest.TestCase):

    def setUp(self):
        self.tour = MagicMock()
        self.velocity = MagicMock()
        self.velocity.current_velocity = MagicMock(return_value=3.0)

        graph = get_test_graph()
        path = shortest_path(graph.graph, 'N1', 'N3')

        self.route = Route(graph.graph, path, self.tour, self.velocity)

    def test_route_update_tour_speed(self):
        self.route.update(1.0)

        self.tour.change_speed.assert_called_once_with(3.0)

    def test_route_update_tour_meters(self):
        self.route.update(1.0)
        self.route.update(100.0)

        self.tour.change_meters.assert_called_with(297.0)

    def test_route_update_tour_azimuth(self):
        self.route.update(1.0)

        self.tour.change_azimuth.assert_called_once_with(math.pi)

    def test_route_update_tour_position(self):
        self.route.update(1.0)

        self.tour.change_position.assert_called_once_with(ANY)

    def test_route_update_tour_doors(self):
        self.route.update(1.0)

        self.tour.change_doors.assert_called_once_with('closed')

    def test_type_is_route(self):
        self.assertEqual('Route', self.route.get_type())

    def test_has_ended_false(self):
        self.route.update(1.0)
        self.route.update(100.0)

        self.assertFalse(self.route.has_ended())

    def test_has_ended_true(self):
        self.route.update(1.0)
        self.route.update(3712.0)
        self.route.update(7423.0)

        self.assertTrue(self.route.has_ended())

    def test_route_length(self):
        self.assertEqual(45, self.route.length)

    def test_to_geojson_contains_type(self):
        self.assertTrue("type" in self.route.to_geojson())

    def test_to_geojson_contains_geometry(self):
        self.assertTrue("geometry" in self.route.to_geojson())

    def test_to_geojson_contains_geometry_type(self):
        self.assertTrue("type" in self.route.to_geojson()["geometry"])

    def test_to_geojson_contains_geometry_type_line_string(self):
        self.assertTrue("LineString", self.route.to_geojson()["geometry"]["type"])

    def test_to_geojson_contains_geometry_coordinates(self):
        self.assertTrue("coordinates" in self.route.to_geojson()["geometry"])

    def test_to_geojson_contains_geometry_coordinates_exist(self):
        self.assertTrue(self.route.to_geojson()["geometry"]["coordinates"])

    def test_to_geojson_contains_style(self):
        self.assertTrue("style" in self.route.to_geojson())

    def test_to_geojson_contains_properties(self):
        self.assertTrue("properties" in self.route.to_geojson())
