import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.routing.dijkstra import shortest_path
from app.app.entities.shuttle import Shuttle
from app.app.routing.graph import Graph
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.models.velocity_model import VelocityModel
from random import random

class FreeFloatShuttle(Shuttle):

    def __init__(self, graph, time, velocity_model, battery_model, bookings):
        super().__init__(graph, time, velocity_model, battery_model)
        self.current_station = 2493824077
        self.bookings = bookings
        self.booking_state = BookingState(bookings, self.current_station)
        self.graph = graph
        self.edge_count = 0
        self.position = graph.nodes.loc[self.current_station]

        self.route = self.__build_tour()

    def first_move(self):
        self.pick_next()

    def pick_next(self):
        self.edge = self.route.edges[self.edge_count]
        self.position = self.edge.origin.geometry
        if self.edge_count < len(self.route.edges) - 1:
            self.edge_count += 1

    def get_route(self):
        return self.route.to_geojson()

    def __build_tour(self):
        destination = self.graph.nodes.iloc[round(random() * len(self.graph.nodes))]
        return shortest_path(self.graph.graph, self.current_station, destination.name)

if __name__ == "__main__":
    shuttle = FreeFloatShuttle(Graph.load_default(), 0, VelocityModel(), BatteryModel())
    print(shuttle.to_geojson())
    for t in range(0, 1000):
        shuttle.move(1)
        print(shuttle.to_geojson())
