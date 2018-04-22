import math
import abc
import random
import pandas as pd
from shapely.geometry import Point, LineString
from graph import Graph
# TODO velocity model (curve, surface, mean/std)
# TODO battery model (battery consumption)

LATITUDE_APPROX = 111320.0


class Entity:
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph, time):
        self.graph = graph
        self.time = time

    @abc.abstractmethod
    def move(self, current_time):
        NotImplementedError()


class Shuttle(Entity):

    def __init__(self, graph, time, velocity_model):
        super().__init__(graph, time)
        start, end = graph.seed()
        self.a = math.atan2(end.y - start.y, end.x - start.x)
        self.position = start
        self.edge = LineString([start, end])
        self.velocity_model = velocity_model

    def current_position(self):
        return self.position

    def move(self, current_time):
        delta_time = current_time - self.time
        degs_per_sec = self.velocity_model.current_velocity()
        x = self.position.x + delta_time * degs_per_sec * math.cos(self.position.y) * math.cos(self.a)
        y = self.position.y + delta_time * degs_per_sec * math.sin(self.a)
        self.position = Point((x, y))
        print(self.position.within(self.edge))


class VelocityModel:
    def __init__(self, min_speed=10.0, max_speed=10.0):
        self.min_speed = min_speed
        self.max_speed = max_speed

    def current_velocity(self):
        """Current random velocity in degrees per second"""
        return random.uniform(self.min_speed, self.max_speed) / LATITUDE_APPROX


if __name__ == '__main__':
    node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
    edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 45], ['4', '1', 25]]
    nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
    nodes.set_index('id')
    edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
    sample_graph = Graph(nodes, edges)
    velocity = VelocityModel()
    shuttle = Shuttle(sample_graph, 0, velocity)
    print(shuttle.current_position())
    for t in range(0, 1000000, 10000):
        shuttle.move(20)
        print(shuttle.current_position())