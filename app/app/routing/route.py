import math
from shapely.geometry import Point
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app.routing.edge import Edge
from app.app.entities.story import Story
from app.app.entities.map_feature import MapFeature


LATITUDE_APPROX = 111320.0


class Route(Story, MapFeature):

    def __init__(self, graph, path, tour, velocity):
        super().__init__()
        self.tour = tour
        self.velocity = velocity
        self.nodes = [graph[node_id] for node_id in path]
        self.edges = self.__edges()
        self.edge_count = 0
        self.time = 0
        self.edge = self.edges[self.edge_count]
        self.position = self.edge.origin.geometry
        self.__length = None
        self.__geojson = None
        self.__has_ended = False

    def update(self, time):
        self.__check_start_time(time)

        meters_per_second = self.velocity.current_velocity()
        degrees_per_second = meters_per_second / LATITUDE_APPROX
        delta_time = (time - self.time)
        delta_degrees = degrees_per_second * delta_time

        x = self.position.x + delta_degrees * math.cos(self.edge.azimuth)
        y = self.position.y + delta_degrees * math.sin(self.edge.azimuth)
        self.position = Point((x, y))

        self.__update_tour(meters_per_second, delta_time)
        self.__check_next()

        self.time = time

    @property
    def length(self):
        if self.__length is None:
            self.__length = sum(edge.distance for edge in self.edges)
        return self.__length

    def get_type(self):
        return 'Route'

    def has_ended(self):
        if self.__has_ended:
            self.__has_ended = False
            self.time = 0
            return True
        return False

    def __check_start_time(self, time):
        if self.time == 0:
            self.time = time

    def __update_tour(self, meters_per_second, delta_time):
        delta_meters = meters_per_second * delta_time
        self.tour.change_speed(meters_per_second)
        self.tour.change_meters(delta_meters)
        self.tour.change_azimuth(self.edge.azimuth)
        self.tour.change_position(self.position)
        self.tour.change_doors('closed')

    def __check_next(self):
        if not self.position.within(self.edge.bounding_box):
            self.__next_edge()

    def __next_edge(self):
        self.edge = self.edges[self.edge_count]
        self.position = self.edge.origin.geometry
        self.edge_count += 1
        if self.edge_count == len(self.edges):
            self.edge_count = 0
            self.__has_ended = True

    def _geometry(self):
        return {
            "type": "LineString",
            "coordinates": [[node.geometry.x, node.geometry.y] for node in self.nodes]
        }

    def _highlight_style(self):
        return {
            "color": self.highlight_color,
            "weight": 5,
            "opacity": 0.7
        }

    def _style(self):
        return {
            "color": "#3182BD",
            "weight": 5,
            "opacity": 0.7
        }

    def _properties(self):
        return {
            "length": self.length,
            "id": "000"
        }

    def __edges(self):
        return [Edge(o, d) for o, d in self.__zip_nodes()]

    def __zip_nodes(self):
        return zip(self.nodes[:-1], self.nodes[1:])

    def __repr__(self):
        return 'Route[length={:.0f}m, origin={}, destination={}]'.format(
            self.length, self.nodes[0], self.nodes[-1])
