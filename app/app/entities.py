import math
import abc
import random

import pandas as pd


# TODO velocity model (curve, surface, mean/std)
# TODO battery model (battery consumption)
from graph import Graph

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
        node, edge = graph.seed()
        start = graph.nodes.loc[edge.iloc[0]['node1']]
        end = graph.nodes.loc[edge.iloc[0]['node2']]
        self.a = math.atan2(end['lat'] - start['lat'], end['lon'] - start['lon'])
        self.x = node['lon'].values[0]
        self.y = node['lat'].values[0]
        self.velocity_model = velocity_model

    def current_position(self):
        return self.x, self.y

    def move(self, current_time):
        delta_time = current_time - self.time
        degrees_per_second = self.velocity_model.current_velocity()
        vx = degrees_per_second * math.cos(self.y)
        vy = degrees_per_second
        self.x = self.x + delta_time * vx * math.cos(self.a)
        self.y = self.y + delta_time * vy * math.sin(self.a)


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
    print(*shuttle.current_position())
    for t in range(0, 20000, 1000):
        shuttle.move(20)
        print(*shuttle.current_position())