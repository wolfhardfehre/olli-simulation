import math
import abc
import random
import pandas as pd
from datetime import datetime
from pytz import timezone, utc
from shapely.geometry import Point, Polygon
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app.routing.graph import Graph


LATITUDE_APPROX = 111320.0
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'


class Entity:
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph, time):
        self.graph = graph
        self.time = time

    @abc.abstractmethod
    def move(self, current_time):
        NotImplementedError()


class Shuttle(Entity):

    def __init__(self, graph, time, velocity_model, battery_model):
        super().__init__(graph, time)
        self.vehicle_id = "EZ10_G2-005"
        self.position, self.edge, self.a, self.start_id, self.end_id = self.__set_edge(graph.seed())
        self.velocity_model = velocity_model
        self.battery_model = battery_model
        self.speed = 0.0

    def current_state(self):
        now = datetime.utcnow()
        local_tz = timezone('Europe/Berlin')
        utc_now = utc.localize(now)
        german = utc_now.astimezone(local_tz)
        properties = {
            'vehicle_id': self.vehicle_id,
            'theta': '{:.4f}'.format(self.a),
            'speed': self.speed,
            'last_seen': german.strftime(DATETIME_FORMAT),
            'created_at': now.strftime(DATETIME_FORMAT),
            'battery': self.battery_model.current_status()
        }
        return self.position, properties

    def move(self, current_time):
        speed = self.velocity_model.current_velocity()
        self.speed = speed * LATITUDE_APPROX
        delta_degrees = speed * (current_time - self.time)
        x = self.position.x + delta_degrees * math.cos(self.a)
        y = self.position.y + delta_degrees * math.sin(self.a)
        self.position = Point((x, y))
        if not self.position.within(self.edge):
            self.__pick_next()
        self.time = current_time

    def __pick_next(self):
        edge = self.graph.next_edge(self.start_id, self.end_id)
        self.position, self.edge, self.a, self.start_id, self.end_id = self.__set_edge(edge)

    @staticmethod
    def __set_edge(edge):
        start, end, start_id, end_id = edge
        azimuth = math.atan2(end.y - start.y, end.x - start.x)
        edge = Polygon(((start.x, start.y), (start.x, end.y), (end.x, end.y), (end.x, start.y)))
        return start, edge, azimuth, start_id, end_id


class VelocityModel:
    def __init__(self, min_speed=10.0, max_speed=10.0):
        self.min_speed = min_speed
        self.max_speed = max_speed

    def current_velocity(self):
        """Current random velocity in degrees per second"""
        return random.uniform(self.min_speed, self.max_speed) / LATITUDE_APPROX


class BatteryModel:
    def __init__(self):
        self.status = 100

    def current_status(self):
        return self.status


if __name__ == '__main__':
    node_data = [['N1', 52.3, 13.4], ['N2', 52.4, 13.4], ['N3', 52.4, 13.3], ['N4', 52.3, 13.3]]
    edge_data = [['N1', 'N2', 30.0], ['N2', 'N3', 20.0], ['N3', 'N4', 45.0], ['N4', 'N1', 25.0]]
    nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
    nodes.set_index('id', inplace=True)
    edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
    shuttle = Shuttle(Graph(nodes, edges), 0, VelocityModel(), BatteryModel())
    print(shuttle.current_state())
    for t in range(0, 100):
        shuttle.move(1)
        print(shuttle.current_state())
