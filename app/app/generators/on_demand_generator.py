import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from app.app.routing.graph import Graph
from app.app.entities.models.velocity_model import VelocityModel
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.free_float_shuttle import FreeFloatShuttle
from app.app.routing.booking import Booking
from random import randint
from app.app.entities.background import Background

class OnDemandGenerator:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = OnDemandGenerator()
        return cls.instance

    def __init__(self):
        self.time = 0.0
        graph = Graph.load_default()
        self.background = Background(graph)
        self.shuttle = FreeFloatShuttle(
            graph, self.time, VelocityModel(), BatteryModel(), self._bookings(graph))
        self.shuttle.first_move()

    def next(self):
        self.time += 1
        self.shuttle.move(self.time)
        return self.shuttle.to_geojson()

    def add_booking(self, booking):
        self.shuttle.add_booking(booking)

    def current_ground_data(self):
        return {
            "type": "FeatureCollection",
            "features": self.background.to_geojson() + [self.shuttle.get_route()] + self.shuttle.booking_state.to_geojson()
        }

    def _bookings(self, graph):
        origin = graph.graph[graph.nodes.iloc[5].name]
        destination = graph.graph[graph.nodes.iloc[100].name]
        bookings = [Booking(origin, destination, 0, 3600)]
        return bookings

